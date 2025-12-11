import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

PRIVATE_KEY_FILE = "student_private.pem"

encrypted_seed_b64 = """EbMvS+at7N4U2Ydc5/tPQ1p+Sfjzn9dDLvz4CJGX7YZQz3XdiJZCC7F2ws6Af5F4oFF2y+7doCY01ttQsLpZTbnE+XVx1w5gJePW72YVIDdF50jBlZm+vwygtxt/CfZ51wGvA1t9Zlr89et/5HBpQ3BEzWuhZeCabFAL5LjQWNJJXTfqKeVHX0PdKVyllsaZf+WTRfLKiUdzBZQ4OfBdW+StDcp6Gb9Xf4cgc4Kbko6oGiXE+LfglI19C9xKIQOjHGSsY5VqJxg4N/UkJY4n+Y/4Yy2vR37S2Q78c5Q6wQz6gWSFj0lAAe3pcdE/VwRGO6MbUWerNS+BHs8JdubMmnQlaALIKLiqG6n8LW7XZE0fyCXdvnGkP5tz7pz00cCZVjRmr3VEWGZ9XLCf4C3sPnCnFjmgFkrS4Rz9MFHSV9o0IdA4yxEfFk/a7Ey5r1GL7vIrex6msdo20CY2qbNDanfVdaXzl9ajfJG+fyt883jdsLvmhwyY298c2PDO8pxsExkbbOQLvSh3sBXOVnOGXRRm/OII20UnDJCpbdUEm/fD/1T4TRHxPH3sdfaUSnQ3C+y2GkKx/B+C5yp5H2kCbxbM5pVmae6lTJyN/8UIELxyWgRLaU2FJixBWkoOOxuTRHnoagunNEVLLXWI9LFTRFlK5jMYlVdRzYX+U2uyd1w="""

# 1. Load private key
with open(PRIVATE_KEY_FILE, "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

# 2. Base64 decode
encrypted_bytes = base64.b64decode(encrypted_seed_b64.strip())

# 3. Decrypt using RSA/OAEP SHA-256
decrypted_bytes = private_key.decrypt(
    encrypted_bytes,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

hex_seed = decrypted_bytes.decode("utf-8").strip().lower()

print("Decrypted seed:", hex_seed)
print("Length:", len(hex_seed))
print("All hex:", all(c in "0123456789abcdef" for c in hex_seed))
