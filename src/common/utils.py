from datetime import datetime
import pytz


def get_time():
    """Get the current time in Indian Standard Time."""
    # Get Indian Standard Time zone
    ist_timezone = pytz.timezone("Asia/Kolkata")

    # Record start time
    ist_time_now = datetime.now(ist_timezone)
    ist_timestamp = ist_time_now.strftime("%Y-%m-%d %H:%M:%S.%f %Z")

    # Get seconds since epoch
    seconds_since_epoch = ist_time_now.timestamp()

    return ist_timestamp, seconds_since_epoch
