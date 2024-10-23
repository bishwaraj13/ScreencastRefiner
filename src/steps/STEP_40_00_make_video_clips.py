# step to make video clips based on each scene
from dotenv import load_dotenv
from common.step_decorator import step_decorator
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

@step_decorator
async def STEP_40_00_make_video_clips(video_id: str, db):
    load_dotenv()

    # Fetch video details
    video_record = db.get_record('ingested_videos', 'video_id', video_id)
    video_file = video_record['video_file']

    # Fetch scenes for the video
    scenes = db.get_records('scenes', 'video_id', video_id)

    print(scenes)

    print("Making video clips for each scene...")
    for scene in scenes:
        step_number = scene['step_number']
        time_start = scene['time_start']
        time_end = scene['time_end']

        # Generate the video clip file path
        clip_file_path = generate_video_clip(video_file,
                                             video_id,
                                             time_start,
                                             time_end)

        # Update the scenes table with the clip file path
        db.update_record('scenes',
                         {'video_id': video_id, 'step_number': step_number},
                         'clip_file_path',
                         clip_file_path)
        

    print("Video clips created successfully")

    return video_id

def generate_video_clip(video_file: str, video_id: str, time_start: float, time_end: float) -> str:
    """
    Generate a video clip from the given video file and save it.
    
    :param video_file: Path to the original video file
    :param video_id: Unique identifier for the video
    :param time_start: Start time of the clip in seconds
    :param time_end: End time of the clip in seconds
    :return: Path to the generated video clip
    """
    # Create a directory for video clips if it doesn't exist
    clips_dir = "video_clips"
    os.makedirs(clips_dir, exist_ok=True)

    # Generate the clip file path
    clip_file_path = os.path.join(clips_dir, f"{video_id}_clip_{time_start}_{time_end}.mp4")

    # Generate the video clip
    ffmpeg_extract_subclip(video_file, time_start, time_end, targetname=clip_file_path)

    return clip_file_path
