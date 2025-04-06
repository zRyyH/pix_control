from datetime import datetime, timezone

def timestamp_para_iso8601(timestamp: int) -> str:
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    data = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    print("Datetime:", data)
    return data