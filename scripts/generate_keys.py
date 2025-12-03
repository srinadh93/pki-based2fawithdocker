from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Generate RSA 4096-bit key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096
)

# Serialize private key to PEM
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()  # no passphrase
)

with open("student_private.pem", "wb") as f:
    f.write(private_pem)

# Generate public key
public_key = private_key.public_key()

# Serialize public key to PEM
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open("student_public.pem", "wb") as f:
    f.write(public_pem)

print("RSA 4096-bit student key pair generated:")
print("- student_private.pem")
print("- student_public.pem")

