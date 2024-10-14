from dotenv import load_dotenv
# from common.connection import VideoDatabase
from common.step_decorator import step_decorator


@step_decorator
async def STEP_10_00_video_preprocessing(video_id: str, db):
    load_dotenv()

    # db = VideoDatabase()
    print("Nothing to do")

    return video_id
