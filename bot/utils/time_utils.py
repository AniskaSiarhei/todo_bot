from datetime import datetime


def is_expired(deadline: str | None) -> bool:

    if not deadline:
        return False

    try:
        dt = datetime.fromisoformat(deadline)
    except ValueError:
        return False

    return dt < datetime.now()
