import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

STUDENT_PRIVATE_KEY_FILE = "student_private.pem"
INSTRUCTOR_PUBLIC_KEY_FILE = "instructor_public.pem"

# === Paste your latest commit hash here ===
COMMIT_HASH = "6bf95ee0aae08fce4854a9b00fd64bc583f60374"  # e.g. "abcd1234ef56..."

def sign_message(message: str) -> bytes:
    with open(STUDENT_PRIVATE_KEY_FILE, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    message_bytes = message.encode("utf-8")  # ASCII/UTF-8 string

    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )

    return signature

def encrypt_with_public_key(data: bytes) -> bytes:
    with open(INSTRUCTOR_PUBLIC_KEY_FILE, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return ciphertext

if __name__ == "__main__":
    print("Commit hash:", COMMIT_HASH)

    signature = sign_message(COMMIT_HASH)
    print("Signature length:", len(signature), "bytes")

    encrypted_signature = encrypt_with_public_key(signature)

    encrypted_signature_b64 = base64.b64encode(encrypted_signature).decode("utf-8")

    print("\neI4pwHljXu+4GXtz0o2kZ28PgDBf35S4QyN5qMIKXiNEjGHIYypkHBXHTl16n3P9eTk5Je7UseDheCkYf5X2grMumqYvu8OVqM2uK46rKhNPsuwy+tjEZBoNDFo2uXRdcpbdPa4Z+7ZZvgn9LRETfDN7rEuc4WhB4MsHrA5j4KnXrmuk4YjOneP5cic2CkC2pCzCKORaZE+nopvbgZjoryYQOE4zLQawWH11D4r1/35+yePf7/nXRWHEpqyJTJy3atxw4goI5Qd81NXKJdBXqdJS+/tn6jlXc0+tmeHeIrGw7EHYHPz0jj7RCLt6LwNRcYN+V4fpVll+9f9myI8bavrpwm8gXLB5ydkySAXvNGh7LAIqvtnJ7G1GAKgncgBXRc3PV2rSq+KpRH3D91u38j4TjmfcTbpQHsDl+o+Wuq8+FFUlTyar6hlO5nYk6sVArAJrGKehncHmGd7+H8k+qKUYasLsT3FpTm29WjeMTx8l/WLKS+T6/3BW4ZO39b2uBj0htMEF+lykw/qGdg2S8W993kwe0PKIg7WWifRpKkINHRu8p0c31aPpwYsGA55Ka3QlOJe4Fc7RpSNeqnUTTqQ/YUrlZ0d0+ake+hwOsTFf14dOsLFoBszNijnjAvlu+U9OZj3x012wH3n97r2H07EC7s35dy3P08zSFMP67H3YbdKQnPkb3swGK60JZr1S585rb/RFewNX5t3hMY/yqHe06eq4IBgkZWNZFaiCeJBZd56gneoDXapBEHXMmHkeKJi+/uqDQDTaU3uz3Y+X0lPi9X1C8NYaUKZLHFktOxqsTMvyNXjd7i+39/7DBuxSgjYdPVOZkaUKmbEwlAfBTEEHk2qskmv1uS9uzWEF3s8XVqyyx+uTKwMEtrkipvy03Jw7sFKe/xddWeBNxTk/H4/89y6XNPTZo7onpy9BaQFvDcT3cjdrI08eXyhdTgfRAR0ivc0uHT71Vuuqpi+jiiHyn6vvdjnE/qgKlAISFQCeUo1Y0AHwmolz8T+Ufz9WxcKAKLAaG2lheftJ2m3ko0X2MBNMDevkHouSt+8kg9xyN2e8E0sZ+EGvB7xaxxlOBGYl1y1r2BHXHYJ6OWyH3RpTZxT+r0kDk6BDqTr8q+EXAYgfL9bCCuSO3khIK0PXGwdw1EgaaT3agKRo0aue2xsA59gfSVHiLXi3qrFQbeZS5jzXXbHAnRoBbxVYcoNqPJCNYol/CpNzTf4rz2MKLpboE5gWzC7d9+kzOQOFilJs7DsndFVa/G6JNt09xaS4z3V8oarQZx96xwomtve/mr25MbXFFGFQrUJwvdgFJ4uZ7bkxoL/qd7GEP5MRhWSg4yKdHfrS0oI8zEO3BhqPKw==")
    print("Encrypted Commit Signature (Base64):")
    print(encrypted_signature_b64)
