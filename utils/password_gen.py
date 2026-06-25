import string
import secrets

def generate(length: int, upper: bool, numbers: bool, symbols: bool) -> str:
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = string.punctuation
    
    
    bucket = lowercase
    if upper:
        bucket += uppercase
    if numbers:
        bucket += digits
    if symbols:
        bucket += special_chars

    requirements = [
        (True,    lambda password: any(c.islower() for c in password)),
        (upper,   lambda password: any(c.isupper() for c in password)),
        (numbers, lambda password: any(c.isdigit() for c in password)),
        (symbols, lambda password: any(c in string.punctuation for c in password))
    ]

    while True:
        password = ''.join(secrets.choice(bucket) for i in range(length))
        checklist = []
        for active, stmt in requirements:
            if active:
                checklist.append(stmt(password))
        
        if all(checklist):
            return password










#https://www.youtube.com/watch?v=XCIBOl3FTKo
#https://docs.python.org/3/library/secrets.html
#https://stackoverflow.com/questions/65366478/python-password-generation-with-complexity-requirement