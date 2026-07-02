import cv2
import face_recognition
import numpy as np
from cryptography.fernet import Fernet

# ---------------- KEY HANDLING ----------------
def get_key():
    try:
        with open("secret.key", "rb") as f:
            key = f.read().strip()
            # Validate key length
            if len(key) != 44:
                raise ValueError("Invalid Fernet key format")
            return key
    except:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as f:
            f.write(key)
        return key


fernet = Fernet(get_key())

# ---------------- FACE CAPTURE ----------------
def capture_face(filename):
    cam = cv2.VideoCapture(0)

    print("Align your face... Press 'c' to capture")

    while True:
        ret, frame = cam.read()
        cv2.imshow("Capture Face", frame)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            enc = face_recognition.face_encodings(frame)
            if len(enc) == 0:
                print("Face not detected! Try again.")
                continue

            np.save(filename, enc[0])
            print("Face saved successfully!")
            break

    cam.release()
    cv2.destroyAllWindows()


# ---------------- FACE VERIFICATION ----------------
def verify_face(saved_file):
    saved_enc = np.load(saved_file)

    cam = cv2.VideoCapture(0)
    print("Align your face for verification...")

    while True:
        ret, frame = cam.read()
        cv2.imshow("Verify Face", frame)

        enc = face_recognition.face_encodings(frame)
        if len(enc) > 0:
            match = face_recognition.compare_faces([saved_enc], enc[0])[0]
            cam.release()
            cv2.destroyAllWindows()
            return match

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    return False


# ---------------- ENCRYPT / DECRYPT ----------------
def encrypt_text(text):
    return fernet.encrypt(text.encode()).decode()

def decrypt_text(token):
    return fernet.decrypt(token.encode()).decode()
