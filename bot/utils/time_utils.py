from datetime import datetime


def is_expired(deadline: str | None) -> bool:

    if not deadline:
        return False

    try:
        deadline_dt = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
    except ValueError:
        return False

    return deadline_dt < datetime.now()
