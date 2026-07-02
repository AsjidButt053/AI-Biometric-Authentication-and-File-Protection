
from utils import verify_face, encrypt_text

if not verify_face("encryptor_face.npy"):
    print("❌ Face mismatch! Encryption denied.")
    exit()

msg = input("Enter text to encrypt: ")
encrypted = encrypt_text(msg)

with open("message.enc", "w") as f:
    f.write(encrypted)

print("\n✔ Message encrypted successfully!")
print("Encrypted Text:", encrypted)
