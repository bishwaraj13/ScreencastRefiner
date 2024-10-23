from dotenv import load_dotenv
from common.step_decorator import step_decorator
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
import os

@step_decorator
async def STEP_60_00_add_voiceover(video_id: str, db):
    load_dotenv()

    # Fetch scenes for the video
    scenes = db.get_records('scenes', 'video_id', video_id)

    # Create a directory for scene video files if it doesn't exist
    video_dir = "video_clips_with_voiceover"
    os.makedirs(video_dir, exist_ok=True)

    for scene in scenes:
        step_number = scene['step_number']

        video_clip = scene["clip_file_path"]
        audio_file = scene["audio_file_path"]

        # Generate the audio file path
        video_file_path = os.path.join(video_dir, f"{video_id}_voiceover_video_{step_number}.mp4")
        add_voiceover(video_clip, audio_file, video_file_path)

        # Update the scenes table with the video file path
        db.update_record('scenes',
                         {'video_id': video_id, 'step_number': step_number},
                         'scene_with_voiceover',
                         video_file_path)
        
    print("Voiceover added to video clips successfully")

    return video_id

def add_voiceover(video_path, audio_path, output_path):
    # Load the video and audio clips
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Get durations
    video_duration = video.duration
    audio_duration = audio.duration

    if audio_duration > video_duration:
        # If audio is longer, extend the first frame of the video
        first_frame = video.to_ImageClip(t=0).set_duration(audio_duration - video_duration)
        extended_video = CompositeVideoClip([first_frame, video.set_start(audio_duration - video_duration)])
        final_video = extended_video.set_audio(audio)
    else:
        # If video is longer, speed up the video
        speed_factor = video_duration / audio_duration
        final_video = video.speedx(factor=speed_factor).set_audio(audio)

    # Write the result to a file
    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')

    # Close the clips
    video.close()
    audio.close()
    final_video.close()




