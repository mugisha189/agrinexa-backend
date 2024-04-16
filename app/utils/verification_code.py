import string
import random
from app.db import db

def generate_verification_code(length=6):
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    return code

def store_verification_code(email, verification_code):
    existing_code = db.verification_codes.find_one({"email": email})
    if existing_code:
        db.verification_codes.update_one({"email": email}, {"$set": {"code": verification_code}})
    else:
        db.verification_codes.insert_one({"email": email, "code": verification_code})

def verify_verification_code(email, verification_code):
    code = db.verification_codes.find_one({"email": email})
    return code and code["code"] == verification_code

def delete_verification_code(email):
    db.verification_codes.delete_one({"email": email})
