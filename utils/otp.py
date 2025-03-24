import random
import string

def generate_otp(length=6):
    # You can adjust the characters used in the OTP
    digits = string.digits  # '0123456789'
    otp = ''.join(random.choices(digits, k=length))
    return otp


