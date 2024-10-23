from dotenv import load_dotenv
from common.step_decorator import step_decorator
import os
from pathlib import Path
from openai import OpenAI

@step_decorator
async def STEP_50_00_generate_audio(video_id: str, db):
    load_dotenv()

    # Load environment variables
    organization_id = os.getenv('OPENAI_ORGANIZATION_ID')
    project_id = os.getenv('OPENAI_PROJECT_ID')
    open_ai_key = os.getenv('OPEN_AI_KEY')

    # Initialize OpenAI client
    client = OpenAI(
        api_key=open_ai_key,
        organization=organization_id,
        project=project_id,
    )

    # Fetch scenes for the video
    scenes = db.get_records('scenes', 'video_id', video_id)

    print("Generating audio for each scene...")
    for scene in scenes:
        step_number = scene['step_number']
        polished_narration = scene['polished_narration']

        # Generate the audio file path
        audio_file_path = generate_audio(client, polished_narration, video_id, step_number)

        # Update the scenes table with the audio file path
        db.update_record('scenes',
                         {'video_id': video_id, 'step_number': step_number},
                         'audio_file_path',
                         audio_file_path)

    print("Audio files generated successfully")

    return video_id

def generate_audio(client, text: str, video_id: str, step_number: int) -> str:
    """
    Generate an audio file from the given text using OpenAI's TTS API and save it.
    
    :param client: OpenAI client
    :param text: Text to be converted to speech
    :param video_id: Unique identifier for the video
    :param step_number: Step number of the scene
    :return: Path to the generated audio file
    """
    # Create a directory for audio files if it doesn't exist
    audio_dir = "audio_clips"
    os.makedirs(audio_dir, exist_ok=True)

    # Generate the audio file path
    audio_file_path = os.path.join(audio_dir, f"{video_id}_audio_{step_number}.mp3")

    # Generate the audio clip
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )

    # Save the audio file
    speech_file_path = Path(audio_file_path)
    response.stream_to_file(speech_file_path)

    return audio_file_path
