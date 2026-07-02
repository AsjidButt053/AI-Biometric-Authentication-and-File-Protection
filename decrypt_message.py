
from utils import verify_face, decrypt_text

if not verify_face("decryptor_face.npy"):
    print("❌ Face mismatch! Decryption denied.")
    exit()

enc = open("message.enc").read().strip()
plain = decrypt_text(enc)

print("\n✔ Decrypted Message:", plain)
