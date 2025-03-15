def recursive_copy(obj: dict | list) -> dict:
    """Copy each record to a new `dict` but skip any keys named `raw` because they cannot be sesrialized to JSON"""

    # print(type(obj), obj)
    if isinstance(obj, dict):
        return {k: self.recursive_copy(v) for k, v in obj.items() if k != "raw"}
    elif isinstance(obj, list):
        return [self.recursive_copy(i) for i in obj]
    else:
        return obj


def seconds_to_dhms(seconds: int) -> tuple[int, int, int, int]:
    """Compute days, hours, minutes, seconds from total seconds"""

    days = seconds // (24 * 3600)
    remaining_seconds = seconds % (24 * 3600)

    hours = remaining_seconds // 3600
    remaining_seconds = remaining_seconds % 3600

    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    return days, hours, minutes, seconds
