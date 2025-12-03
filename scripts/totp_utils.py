import pyotp
import base64

def hex_to_base32(hex_seed: str) -> str:
    """
    Convert 64-character hex seed to base32 string for TOTP
    """
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    return base32_seed

def generate_totp_code(hex_seed: str) -> str:
    """
    Generate current TOTP code from hex seed
    """
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)  # 6-digit, 30s period
    return totp.now()

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verify TOTP code with ±1 period tolerance
    """
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)
    return totp.verify(code, valid_window=valid_window)
