from dotenv import load_dotenv
from common.step_decorator import step_decorator
from common.static import prompt_template
import google.generativeai as genai
import os
import json
import re

def load_json_from_string(json_string):
    """Load JSON data from a string, with support for code block markers and partial parsing."""
    # Remove code block markers if present
    json_string = json_string.strip().lstrip("```json").rstrip("```")

    # Remove unexpected double quotes used to highlight words
    pattern = r'\s"([^"]+)"\s'
    json_string = re.sub(pattern, r" \1 ", json_string)

    # parse the entire JSON string
    parsed_json = json.loads(json_string)
    print(f"Full JSON parsed successfully: {parsed_json}")

    # if the parsed JSON is not successful, it will raise error
    return parsed_json


@step_decorator
async def STEP_30_00_make_scenes(video_id: str, db):
    load_dotenv()
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 100000,
        "response_mime_type": "application/json",
    }

    transcription_record = db.get_record(
        'transcriptions', 'video_id', video_id)

    transcript_dict = str(transcription_record['transcript_dict'])

    final_prompt = prompt_template.replace('{transcription_dict}', transcript_dict)

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    response = model.generate_content(final_prompt)

    response_json = load_json_from_string(response.text)

    for index, step in enumerate(response_json['steps']):
        title = step['title']
        time_start = step['time_start']
        time_end = step['time_end']
        original_narration = step['original_narration']
        polished_narration = step['polished_narration']

        db.add_scene(
            video_id,
            index,
            title,
            time_start,
            time_end,
            original_narration,
            polished_narration
        )

    return video_id
