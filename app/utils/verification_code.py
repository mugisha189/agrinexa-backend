
def generate_verification_code(length=6):
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for i in range(length))
    return code


def store_verification_code(email, verification_code):
    db.verification_codes.insert_one({"email": email, "code": verification_code})