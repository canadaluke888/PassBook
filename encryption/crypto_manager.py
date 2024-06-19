import os
from cryptography.fernet import Fernet


class CryptoManager:
    def __init__(self, key_file='PassBookPassword/key.key'):
        self.key_file = key_file
        self.key = self.load_key()

    def generate_key(self):
        key = Fernet.generate_key()
        os.makedirs(os.path.dirname(self.key_file), exist_ok=True)  # Ensure the directory exists
        with open(self.key_file, 'wb') as key_file:
            key_file.write(key)
        self.key = key

    def load_key(self):
        try:
            with open(self.key_file, 'rb') as key_file:
                return key_file.read()
        except FileNotFoundError:
            self.generate_key()
            return self.key

    def save_key(self):
        with open(self.key_file, 'wb') as key_file:
            key_file.write(self.key)

    def update_key(self):
        self.generate_key()

    def encrypt(self, message: str) -> bytes:
        f = Fernet(self.key)
        return f.encrypt(message.encode())

    def decrypt(self, encrypted_message: bytes) -> str:
        f = Fernet(self.key)
        return f.decrypt(encrypted_message).decode()
