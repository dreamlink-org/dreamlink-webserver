from datetime import datetime, timezone

def log(msg):
    utc_now = datetime.now(timezone.utc)
    print(f"[{utc_now:%Y-%m-%d %H:%M:%S}] {msg}")