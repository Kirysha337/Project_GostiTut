import base64
import os
import hashlib

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from config import GOST_KEY_ENV


def sha256_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_aes_key() -> bytes:
    """Берём ключ для шифрования паспортов."""
    if GOST_KEY_ENV:
        try:
            return base64.b64decode(GOST_KEY_ENV)
        except Exception:
            print("ERROR: GOST_KEY exists but is not valid base64 — using/generating local key.")

    # Пытаемся взять ключ из файла, если его нет — создаём новый
    path = "./enc_key.bin"
    if os.path.exists(path):
        return open(path, "rb").read()

    # Генерируем временный ключ и сохраняем рядом с программой
    key = AESGCM.generate_key(bit_length=256)
    try:
        with open(path, "wb") as f:
            f.write(key)
        os.chmod(path, 0o600)
        print(f"[warn] AES key not found in env: generated temporary key saved to {path}. "
              f"For production put base64 key into GOST_KEY.")
    except Exception as e:
        print("Failed to save temporary key:", e)
    return key


AES_KEY = load_aes_key()


def aes_encrypt(plaintext: bytes):
    aes = AESGCM(AES_KEY)
    nonce = os.urandom(12)
    ct = aes.encrypt(nonce, plaintext, None)
    return nonce, ct


def aes_decrypt(nonce: bytes, ct: bytes):
    aes = AESGCM(AES_KEY)
    return aes.decrypt(nonce, ct, None)


