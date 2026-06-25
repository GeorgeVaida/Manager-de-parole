import pytest
import os
import json
from utils import crypto

def test_encryption_decryption():
    test_key = crypto.generate_key("STRONGPASSWORD".encode('utf-8'), os.urandom(16))

    logins = {
        "title" : "amazon",
        "username" : "myUsername",
        "password": "bestPassword123",
    }

    ciphertext = crypto.encrypt_data(test_key, logins["title"], logins["username"], logins["password"])
    assert "bestPassword123" not in str(ciphertext)


    decrypted = crypto.decrypt_data(test_key, ciphertext, logins["title"])
    assert decrypted["username"] == logins["username"]
    assert decrypted["password"] == logins["password"]
    
    

def test_wrong_key():
    test_key = crypto.generate_key("STRONGPASSWORD".encode('utf-8'), os.urandom(16))
    wrong_key = crypto.generate_key("wrongkey".encode('utf-8'), os.urandom(16))

    logins = {
        "title" : "amazon",
        "username" : "myUsername",
        "password": "bestPassword123",
    }

    ciphertext = crypto.encrypt_data(test_key, logins["title"], logins["username"], logins["password"])

    with pytest.raises(Exception):
        crypto.decrypt_data(wrong_key, ciphertext, logins['title'])
    

def test_assoc_data():
    test_key = crypto.generate_key("STRONGPASSWORD".encode('utf-8'), os.urandom(16))

    logins = {
        "title" : "amazon",
        "username" : "myUsername",
        "password": "bestPassword123",
    }

    ciphertext = crypto.encrypt_data(test_key, logins["title"], logins["username"], logins["password"])
    
    with pytest.raises(Exception):
        crypto.decrypt_data(test_key, ciphertext, "google")