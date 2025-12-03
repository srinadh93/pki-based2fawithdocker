import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import os

# Paths
PRIVATE_KEY_FILE = "student_private.pem"
ENCRYPTED_SEED_FILE = "encrypted_seed.txt"
OUTPUT_SEED_FILE = "data/seed.txt"  # persistent storage in Docker

# Ensure /data exists
os.makedirs("data", exist_ok=True)

# 1. Load private key
with open(PRIVATE_KEY_FILE, "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

# 2. Load encrypted seed
with open(ENCRYPTED_SEED_FILE, "r") as f:
    encrypted_seed_b64 = f.read().strip()

# 3. Base64 decode
encrypted_seed_bytes = base64.b64decode(encrypted_seed_b64)

# 4. Decrypt using RSA/OAEP with SHA-256
try:
    decrypted_bytes = private_key.decrypt(
        encrypted_seed_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    # 5. Convert to string
    decrypted_seed = decrypted_bytes.decode("utf-8").lower()
    
    # Validate 64-character hex
    if len(decrypted_seed) != 64 or not all(c in "0123456789abcdef" for c in decrypted_seed):
        raise ValueError("Decrypted seed is not a valid 64-character hex string")

    # 6. Save to /data/seed.txt
    with open(OUTPUT_SEED_FILE, "w") as f:
        f.write(decrypted_seed)

    print(f"✅ Seed decrypted and saved to {OUTPUT_SEED_FILE}")
except Exception as e:
    print("❌ Decryption failed:", str(e))
