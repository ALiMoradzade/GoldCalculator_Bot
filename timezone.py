import datetime
import pytz

# Install pytz


def tehran_datetime(strftime: str) -> str:
    timeZone = pytz.timezone("Asia/Tehran")
    timeZone_now = datetime.datetime.now(timeZone).strftime(strftime)
    return timeZone_now
