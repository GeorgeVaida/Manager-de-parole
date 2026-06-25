import os
import hashlib
import json
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def generate_salt() -> bytes:
    return os.urandom(16)



def generate_key(password: bytearray, salt : bytearray) -> bytes:
    kdf = Argon2id(salt=salt, length=32, iterations=3, lanes=4, memory_cost=64 * 1024, ad=None, secret=None)
    key = kdf.derive(password)
    

    return key

def hash_key(key : bytes) -> bytes:
    return hashlib.sha256(key).digest()


def encrypt_data(key : bytearray, title: str, username: str, password:str) -> bytes:
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    
    dictionary = {"username" : username, "password" : password}
    json_dictionary  = json.dumps(dictionary).encode('utf-8')
    
    encrypted_data = aesgcm.encrypt(nonce=nonce, data=json_dictionary, associated_data=title.encode('utf-8'))
    
    return nonce + encrypted_data


def decrypt_data(key: bytearray, encrypted_data: bytes, assoc_data:str) -> dict:
    aesgcm = AESGCM(key)
    try:
        nonce = encrypted_data[:12]
        
        json_bytes = aesgcm.decrypt(nonce, encrypted_data[12:], assoc_data.encode('utf-8'))
        text = json_bytes.decode('utf-8')

        return json.loads(text)
    
    except Exception as e:
        raise ValueError(f"Data integrity failed for {assoc_data}, Error: {e}")


def encrypt_2fa(key: bytearray, secret: bytes) -> bytes:
    nonce = os.urandom(12)
    aesgcm = AESGCM(key)
    
    encrypted_data = aesgcm.encrypt(nonce=nonce, data=secret, associated_data=None)
    
    return nonce + encrypted_data

def decrypt_2fa(key: bytearray, encrypted_data: bytes, assoc_data=None) -> bytes:
    aesgcm = AESGCM(key)

    nonce = encrypted_data[:12]
    secret = aesgcm.decrypt(nonce, encrypted_data[12:], associated_data=None)

    return secret