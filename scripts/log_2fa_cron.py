from datetime import datetime
from scripts.totp_utils import generate_totp_code

SEED_FILE = "/data/seed.txt"
LOG_FILE = "/cron/last_code.txt"

try:
    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()

    code = generate_totp_code(hex_seed)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - 2FA Code: {code}\n")

except FileNotFoundError:
    print("Seed file not found")
except Exception as e:
    print("Error:", str(e))
