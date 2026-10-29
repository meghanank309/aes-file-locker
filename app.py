
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# File format: magic header + 12-byte nonce + encrypted data
MAGIC = b"MAF1"
NONCE_SIZE = 12
KEY_SIZE = 32  # 32 bytes = 256-bit AES key


class AESFileLocker:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini AES File Locker")
        self.root.geometry("540x360")
        self.root.resizable(False, False)

        self.file_path = tk.StringVar()
        self.key_text = tk.StringVar()

        tk.Label(
            root, text="Mini AES File Locker",
            font=("Arial", 18, "bold")
        ).pack(pady=(15, 5))

        tk.Label(
            root, text="Encrypt and decrypt files securely",
            font=("Arial", 10)
        ).pack(pady=(0, 15))

        file_frame = tk.Frame(root)
        file_frame.pack(fill="x", padx=20)

        tk.Entry(
            file_frame, textvariable=self.file_path, width=43
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            file_frame, text="Browse", command=self.browse_file
        ).pack(side="left")

        tk.Label(root, text="AES-256 key (keep it secret):").pack(
            anchor="w", padx=20, pady=(18, 5)
        )

        key_frame = tk.Frame(root)
        key_frame.pack(fill="x", padx=20)

        tk.Entry(
            key_frame, textvariable=self.key_text, width=53
        ).pack(side="left", fill="x", expand=True)

        tk.Button(
            key_frame, text="Generate Key",
            command=self.generate_key
        ).pack(side="left", padx=(8, 0))

        button_frame = tk.Frame(root)
        button_frame.pack(pady=22)

        tk.Button(
            button_frame, text="Encrypt File",
            width=16, command=self.encrypt_file
        ).pack(side="left", padx=8)

        tk.Button(
            button_frame, text="Decrypt File",
            width=16, command=self.decrypt_file
        ).pack(side="left", padx=8)

        self.status = tk.StringVar(value="Ready")
        tk.Label(
            root, textvariable=self.status,
            fg="darkgreen", wraplength=490
        ).pack(pady=5)

        tk.Label(
            root, text="Keep your key safe. Without it, decryption is impossible.",
            font=("Arial", 9), wraplength=490
        ).pack(pady=5)

    def browse_file(self):
        path = filedialog.askopenfilename(
            title="Select a file"
        )
        if path:
            self.file_path.set(path)
            self.status.set("File selected.")

    def generate_key(self):
        key = AESGCM.generate_key(bit_length=256)
        self.key_text.set(key.hex())
        self.status.set(
            "New 256-bit key generated. Save it somewhere safe."
        )

    def get_key(self):
        try:
            key = bytes.fromhex(self.key_text.get().strip())
            if len(key) != KEY_SIZE:
                raise ValueError
            return key
        except ValueError:
            raise ValueError(
                "Invalid key. Generate a key or enter the original "
                "64-character hexadecimal key."
            )

    def encrypt_file(self):
        source = self.file_path.get().strip()
        if not source or not os.path.isfile(source):
            messagebox.showerror("Error", "Please select an existing file.")
            return

        try:
            key = self.get_key()
            with open(source, "rb") as file:
                data = file.read()

            nonce = os.urandom(NONCE_SIZE)
            encrypted = AESGCM(key).encrypt(nonce, data, MAGIC)

            destination = filedialog.asksaveasfilename(
                title="Save encrypted file",
                initialfile=os.path.basename(source) + ".aes",
                defaultextension=".aes",
                filetypes=[("AES encrypted files", "*.aes"),
                           ("All files", "*.*")]
            )
            if not destination:
                self.status.set("Encryption cancelled.")
                return

            if os.path.abspath(destination) == os.path.abspath(source):
                raise ValueError("Choose a different output file.")

            with open(destination, "wb") as file:
                file.write(MAGIC + nonce + encrypted)

            self.status.set("Encryption successful.")
            messagebox.showinfo(
                "Success", f"Encrypted file saved:\n{destination}"
            )

        except Exception as error:
            messagebox.showerror("Encryption failed", str(error))

    def decrypt_file(self):
        source = self.file_path.get().strip()
        if not source or not os.path.isfile(source):
            messagebox.showerror("Error", "Please select an existing file.")
            return

        try:
            key = self.get_key()

            with open(source, "rb") as file:
                payload = file.read()

            minimum_size = len(MAGIC) + NONCE_SIZE + 16
            if len(payload) < minimum_size or not payload.startswith(MAGIC):
                raise ValueError("This is not a valid encrypted file.")

            nonce_start = len(MAGIC)
            nonce = payload[nonce_start:nonce_start + NONCE_SIZE]
            ciphertext = payload[nonce_start + NONCE_SIZE:]

            # AES-GCM verifies the key and detects altered ciphertext.
            plaintext = AESGCM(key).decrypt(nonce, ciphertext, MAGIC)

            suggested_name = os.path.basename(source)
            if suggested_name.endswith(".aes"):
                suggested_name = suggested_name[:-4] + "_decrypted"
            else:
                suggested_name += "_decrypted"

            destination = filedialog.asksaveasfilename(
                title="Save decrypted file",
                initialfile=suggested_name,
                filetypes=[("All files", "*.*")]
            )
            if not destination:
                self.status.set("Decryption cancelled.")
                return

            if os.path.abspath(destination) == os.path.abspath(source):
                raise ValueError("Choose a different output file.")

            with open(destination, "wb") as file:
                file.write(plaintext)

            self.status.set("Decryption successful.")
            messagebox.showinfo(
                "Success", f"Decrypted file saved:\n{destination}"
            )

        except Exception:
            messagebox.showerror(
                "Decryption failed",
                "Decryption failed. Check your key and file. "
                "The encrypted data may be damaged or modified."
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = AESFileLocker(root)
    root.mainloop()
