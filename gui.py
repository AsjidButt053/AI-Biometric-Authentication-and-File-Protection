import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import sys
import os
from cryptography.fernet import Fernet
from utils import verify_face, get_key

# ---------------- REGISTER FUNCTIONS ----------------
def run_script(script_name):
    subprocess.Popen([sys.executable, script_name])

def register_encryptor():
    messagebox.showinfo("Step 1", "Register Encryptor Face")
    run_script("register_encryptor.py")

def register_decryptor():
    messagebox.showinfo("Step 2", "Register Decryptor Face")
    run_script("register_decryptor.py")

# ---------------- ENCRYPT ----------------
def encrypt_text():
    plaintext = input_text.get("1.0", tk.END).strip()

    if not plaintext:
        messagebox.showerror("Error", "Enter text to encrypt!")
        return

    messagebox.showinfo("Face Verification", "Verifying ENCRYPTOR face")
    if not verify_face("encryptor_face.npy"):
        messagebox.showerror("Access Denied", "Encryptor face not verified!")
        return

    key = get_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(plaintext.encode()).decode()

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, encrypted)

    with open("encrypted_message.txt", "w") as f:
        f.write(encrypted)

    messagebox.showinfo("Success", "Text Encrypted Successfully")

# ---------------- DECRYPT ----------------
def decrypt_text():
    if not os.path.exists("encrypted_message.txt"):
        messagebox.showerror("Error", "No encrypted message found!")
        return

    encrypted = output_text.get("1.0", tk.END).strip()
    if not encrypted:
        encrypted = open("encrypted_message.txt").read()

    messagebox.showinfo("Face Verification", "Verifying DECRYPTOR face")
    if not verify_face("decryptor_face.npy"):
        messagebox.showerror("Access Denied", "Decryptor face not verified!")
        return

    key = get_key()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted.encode()).decode()

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, decrypted)

    messagebox.showinfo("Success", "Text Decrypted Successfully")

# ---------------- GUI DESIGN ----------------
root = tk.Tk()
root.title("Face Recognition Secure Encryption System")
root.geometry("750x550")
root.configure(bg="#1e1e1e")

tk.Label(
    root,
    text="🔐 Face-Based Secure Encryption & Decryption",
    font=("Arial", 15, "bold"),
    fg="white",
    bg="#1e1e1e"
).pack(pady=10)

# Register buttons
btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Register Encryptor Face", width=25,
          command=register_encryptor, bg="#007acc", fg="white").pack(side="left", padx=10)

tk.Button(btn_frame, text="Register Decryptor Face", width=25,
          command=register_decryptor, bg="#007acc", fg="white").pack(side="left", padx=10)

# Input text
tk.Label(root, text="Enter Plain Text:", fg="white", bg="#1e1e1e").pack(pady=5)
input_text = scrolledtext.ScrolledText(root, height=5, width=80)
input_text.pack()

# Encrypt / Decrypt buttons
action_frame = tk.Frame(root, bg="#1e1e1e")
action_frame.pack(pady=10)

tk.Button(action_frame, text="🔒 Encrypt", width=20,
          command=encrypt_text, bg="#28a745", fg="white").pack(side="left", padx=15)

tk.Button(action_frame, text="🔓 Decrypt", width=20,
          command=decrypt_text, bg="#dc3545", fg="white").pack(side="left", padx=15)

# Output text
tk.Label(root, text="Encrypted / Decrypted Output:", fg="white", bg="#1e1e1e").pack(pady=5)
output_text = scrolledtext.ScrolledText(root, height=7, width=80)
output_text.pack()

tk.Label(
    root,
    text="Course: Information Security | Biometric Cryptography",
    fg="gray",
    bg="#1e1e1e"
).pack(side="bottom", pady=10)

root.mainloop()
