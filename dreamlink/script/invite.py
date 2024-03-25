from dreamlink.lib.db import get_connection
from argparse import ArgumentParser
from datetime import datetime, timedelta, timezone
from secrets import token_hex

parser = ArgumentParser()
parser.add_argument(
    "expiry", 
    type = int, 
    nargs = "?", 
    default = 24 * 7
)

def generate_invite_code(num_hours):
    token = token_hex(8).upper()
    utc_now = datetime.now(timezone.utc)
    expiry = utc_now + timedelta(hours = num_hours)
    with get_connection() as conn:
        conn.execute(lambda col: f"""
            INSERT INTO "user_invite" (
                "token", "created_at", "expires_at"
            ) VALUES (
                {col(token)},
                {col(utc_now)},
                {col(expiry)}
            )
        """)
    print(f"Generated invite code: {token}")

if __name__ == "__main__":
    args = parser.parse_args()
    generate_invite_code(args.expiry)
