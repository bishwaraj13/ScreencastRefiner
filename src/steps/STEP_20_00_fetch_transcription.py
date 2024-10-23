import os
from dotenv import load_dotenv
from rev_ai import apiclient
from common.step_decorator import step_decorator
import asyncio


@step_decorator
async def STEP_20_00_fetch_transcription(video_id: str, db):
    load_dotenv()

    # Fetch video details
    video_record = db.get_record('ingested_videos', 'video_id', video_id)
    audio_file = video_record['audio_file']

    # Get Rev AI access token from environment variable
    rev_access_token = os.getenv('REV_ACCESS_TOKEN')
    if not rev_access_token:
        raise ValueError("REV_ACCESS_TOKEN not found in environment variables")

    # Initialize Rev AI client
    client = apiclient.RevAiAPIClient(rev_access_token)

    print("Submitting audio file for transcription...")
    job = client.submit_job_local_file(audio_file)

    print(f"Transcription job submitted. Job ID: {job.id}")

    # Wait for the job to complete
    job_details = client.get_job_details(job.id)
    while job_details.status != 'transcribed':
        print(f"Job status: {job_details.status}")
        await asyncio.sleep(10)  # Wait for 10 seconds before checking again
        job_details = client.get_job_details(job.id)

    print("Transcription completed. Fetching results...")

    # Get the transcript
    transcript_dict = client.get_transcript_json(job.id)

    db.add_transcription(
        video_id, transcript_dict)

    print("Transcription stored successfully")

    return video_id
