from datetime import datetime, timedelta, timezone


def get_now_w_tz() -> datetime:
    return datetime.now(tz=timezone.utc)
