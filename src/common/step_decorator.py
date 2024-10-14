from datetime import datetime
import pytz
from contextlib import contextmanager
from common.connection import VideoDatabase
from functools import wraps
from .static import requirements_dict
from dotenv import load_dotenv
import uuid


@contextmanager
def timing_context(step_name, video_id, db):
    ist_timezone = pytz.timezone("Asia/Kolkata")
    start_time = datetime.now(ist_timezone)
    print(f"Start step: {step_name}")
    print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S.%f %Z')}")
    try:
        yield
    finally:
        end_time = datetime.now(ist_timezone)
        duration = end_time - start_time
        print(f"End step: {step_name}")
        print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S.%f %Z')}")
        print(f"Duration: {duration.total_seconds():.3f} seconds")


def step_decorator(function):
    @wraps(function)
    async def wrapper(video_id: str, db=VideoDatabase()):
        load_dotenv()
        with timing_context(function.__name__, video_id, db):
            result = await function(db=db, video_id=video_id)
        return result
    return wrapper
