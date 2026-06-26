from utils import dbconn, crypto
from core import session


def auth(password: str):

    user_entry = dbconn.fetch_user()

    if user_entry is None:

        salt = crypto.generate_salt()
        session.KEY = crypto.generate_key(password, salt=salt)
        key_hash = crypto.hash_key(session.KEY)

        dbconn.setup_user(salt, key_hash)
        return "SETUP_OK"
    else:
        user_salt = user_entry[0]
        user_hash = user_entry[1]

        generated_key = crypto.generate_key(password, user_salt)
        key_hash = crypto.hash_key(generated_key)


        if (key_hash == user_hash):
            session.KEY = generated_key
            
            if dbconn.get_2fa() is not None:
                return "2FA"
            else: 
                return "LOGIN_OK"
        else:
            del generated_key
            return "LOGIN_FAIL"