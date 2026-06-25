import string

def calculate(password : str) -> int:
    score = 0
    length = len(password)

    checks = [
        False, # Lower case
        False, # upper case
        False, # digits
        False  # special char
    ]
    for c in password:
        if c.islower():
            checks[0] = True
        elif c.isupper():
            checks[1] = True
        elif c.isdigit():
            checks[2] = True
        elif c in string.punctuation:
            checks[3] = True

    if length > 8: score += 1
    if length > 12: score += 1
    if length > 16: score += 1

    for b in checks:
        if b: score += 1
        
    return score