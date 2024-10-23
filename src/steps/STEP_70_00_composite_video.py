from dotenv import load_dotenv
from common.step_decorator import step_decorator
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

@step_decorator
async def STEP_70_00_composite_video(video_id: str, db):
    load_dotenv()

    # Fetch scenes for the video
    scenes = db.get_records('scenes', 'video_id', video_id)

    # Create a directory for storing composite video
    video_dir = "composite_videos"
    os.makedirs(video_dir, exist_ok=True)

    scene_clips = []

    for scene in scenes:
        step_number = scene['step_number']
        scene_with_voiceover = scene["scene_with_voiceover"]

        # Load the video clip (which already includes the voiceover)
        video_clip = VideoFileClip(scene_with_voiceover)
        scene_clips.append(video_clip)

    # Concatenate all scene clips
    final_video = concatenate_videoclips(scene_clips)

    # Write the final composite video
    output_path = os.path.join(video_dir, f"{video_id}_composite.mp4")
    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')

    # Close all clips
    for clip in scene_clips:
        clip.close()
    final_video.close()

    print("Composite video created successfully")

    return video_id