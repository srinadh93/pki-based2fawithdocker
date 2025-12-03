from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from scripts.totp_utils import generate_totp_code, verify_totp_code

app = FastAPI()
SEED_FILE = "data/seed.txt"
PRIVATE_KEY_FILE = "student_private.pem"

# Request model
class DecryptSeedRequest(BaseModel):
    encrypted_seed: str

class Verify2FARequest(BaseModel):
    code: str

# Endpoint 1: Decrypt seed
@app.post("/decrypt-seed")
def decrypt_seed(request: DecryptSeedRequest):
    if not os.path.exists(PRIVATE_KEY_FILE):
        raise HTTPException(status_code=500, detail="Private key not found")

    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import padding

    try:
        with open(PRIVATE_KEY_FILE, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)

        encrypted_bytes = base64.b64decode(request.encrypted_seed)
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        decrypted_seed = decrypted_bytes.decode("utf-8").lower()

        if len(decrypted_seed) != 64 or not all(c in "0123456789abcdef" for c in decrypted_seed):
            raise ValueError("Invalid decrypted seed")

        os.makedirs("data", exist_ok=True)
        with open(SEED_FILE, "w") as f:
            f.write(decrypted_seed)

        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Decryption failed")

# Endpoint 2: Generate 2FA
@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()

    code = generate_totp_code(hex_seed)
    # Remaining validity seconds
    import time
    valid_for = 30 - int(time.time()) % 30

    return {"code": code, "valid_for": valid_for}

# Endpoint 3: Verify 2FA
@app.post("/verify-2fa")
def verify_2fa(request: Verify2FARequest):
    if not request.code:
        raise HTTPException(status_code=400, detail="Missing code")

    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()

    is_valid = verify_totp_code(hex_seed, request.code)
    return {"valid": is_valid}
