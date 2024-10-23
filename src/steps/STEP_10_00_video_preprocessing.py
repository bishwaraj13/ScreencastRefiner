from dotenv import load_dotenv
from common.step_decorator import step_decorator
from moviepy.editor import VideoFileClip
import os


@step_decorator
async def STEP_10_00_video_preprocessing(video_id: str, db):
    load_dotenv()

    # fetch video details
    video_record = db.get_record(
        'ingested_videos', 'video_id', video_id)

    video_file = video_record['video_file']

    print("Performing some preprocessing tasks...")

    # Get video metadata
    video_metadata = extract_video_metadata(video_file)

    # Update the ingested_videos table with the video metadata   
    db.update_record(
        'ingested_videos',
        {'video_id': video_id},
        'video_metadata',
        video_metadata)

    # Generate audio from video
    audio_file = generate_audio_from_video(video_file, video_id)

    # Update the audio_file field in the ingested_videos table
    db.update_record(
        'ingested_videos',
        {'video_id': video_id},
        'audio_file',
        audio_file)

    print("Video preprocessing completed successfully")

    return video_id


def generate_audio_from_video(video_file: str, video_id: str) -> str:
    """
    Generate audio from the given video file and save it.
    """
    video = VideoFileClip(video_file)
    audio = video.audio

    # Create a directory for audio files if it doesn't exist
    audio_dir = "audio_files"
    os.makedirs(audio_dir, exist_ok=True)

    # Generate the audio file path
    audio_file = os.path.join(audio_dir, f"{video_id}_audio.mp3")

    # Write the audio to a file
    audio.write_audiofile(audio_file)

    # Close the video and audio objects
    audio.close()
    video.close()

    return audio_file


def extract_video_metadata(video_file):
    """Extract basic metadata from the video file."""
    with VideoFileClip(video_file) as video:
        return {
            'duration': video.duration,
            'fps': video.fps,
            'size': video.size,
            'audio_fps': video.audio.fps if video.audio else None,
            'audio_nchannels': video.audio.nchannels if video.audio else None
        }
