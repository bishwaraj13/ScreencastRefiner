from dotenv import load_dotenv
# from common.connection import VideoDatabase
from common.step_decorator import step_decorator


@step_decorator
async def STEP_10_00_video_preprocessing(video_id: str, db):
    load_dotenv()

    print("Starting video preprocessing...")

    # Simulate some processing
    print("Performing some preprocessing tasks...")

    # Randomly decide whether to raise an error
    if 0.1 < 0.5:  # 50% chance of raising an error
        raise ValueError("Random error occurred during video preprocessing")

    print("Video preprocessing completed successfully")

    return video_id
