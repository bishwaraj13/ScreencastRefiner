from steps.STEP_10_00_video_preprocessing import STEP_10_00_video_preprocessing
from steps.STEP_20_00_fetch_transcription import STEP_20_00_fetch_transcription
from steps.STEP_30_00_make_scenes import STEP_30_00_make_scenes
from steps.STEP_40_00_make_video_clips import STEP_40_00_make_video_clips
from steps.STEP_50_00_generate_audio import STEP_50_00_generate_audio
from steps.STEP_60_00_add_voiceover import STEP_60_00_add_voiceover
from steps.STEP_70_00_composite_video import STEP_70_00_composite_video

if __name__ == '__main__':
    import asyncio

    # asyncio.run(STEP_10_00_video_preprocessing(
    #     'fdebd853-a815-46ad-bbd2-335471d2d640'))

    # asyncio.run(STEP_20_00_fetch_transcription(
    #     'fdebd853-a815-46ad-bbd2-335471d2d640'))

    # asyncio.run(STEP_30_00_make_scenes(
    #     'fdebd853-a815-46ad-bbd2-335471d2d640'))

    # asyncio.run(STEP_40_00_make_video_clips(
    #     'fdebd853-a815-46ad-bbd2-335471d2d640'))

    # asyncio.run(STEP_50_00_generate_audio(
    #     'fdebd853-a815-46ad-bbd2-335471d2d640'))
    
    # asyncio.run(STEP_60_00_add_voiceover(
    #     'fdebd853-a815-46ad-bbd2-335471d2d640'))
    
    asyncio.run(STEP_70_00_composite_video(
        'fdebd853-a815-46ad-bbd2-335471d2d640'))
    
