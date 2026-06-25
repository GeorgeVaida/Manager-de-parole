import pyotp
import qrcode
import base64
from io import BytesIO


def generate_2fa():

    random = pyotp.random_base32()

    totp = pyotp.TOTP(random)
    uri = totp.provisioning_uri(name="user", issuer_name="password manager")

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(uri)
    qr.make(fit=True)
    
    
    img = qr.make_image(fill_color="black", back_color="white")
    memory_buffer = BytesIO()
    img.save(memory_buffer, format="png")
    
    base64_qr = base64.b64encode(memory_buffer.getvalue()).decode("utf-8")

    return {
        "qr_image": base64_qr,
        "secret": random
    }

def confirm_and_save(secret: bytes ,code: str) -> tuple[bool, str]:
    
    totp = pyotp.TOTP(secret)
    
    if totp.verify(code):
        from core import session
        from utils.dbconn import save_2fa
        from utils.crypto import encrypt_2fa

        encrypted_secret = encrypt_2fa(session.KEY, secret.encode('utf-8'))
        if save_2fa(encrypted_secret) == False:
            return [False, "DB_ERROR"]
        else:
            return [True, "OK"]
    else:
        return False, "WRONG_CODE"


def is_enabled() -> bool:
    from utils.dbconn import get_2fa
    if get_2fa() is None:
        return False
    else:
        return True
    
def get_and_verify(code):
    from core import session
    from utils.dbconn import get_2fa
    from utils.crypto import decrypt_2fa

    encrypted_secret = get_2fa()
    secret = decrypt_2fa(session.KEY, encrypted_secret)
    
    totp = pyotp.TOTP(secret)
    if totp.verify(code):
        return True
    else:
        return False


def disable():
    from utils.dbconn import delete_2fa

    response = delete_2fa()
    return response