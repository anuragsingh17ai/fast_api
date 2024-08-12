from pydantic import BaseModel, Field, EmailStr, field_validator
from fastapi import FastAPI, HTTPException, Depends
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional
import random
import string

app = FastAPI()

otp_storage = {}

un_official_domain = [
    "gmail.com",
    "yahoo.com",
    "example.com"  
]

class UserVerificationBase(BaseModel):
    email: EmailStr
    phone_no: Optional[PhoneNumber] = None

    @field_validator('email')
    def is_official_mail(cls, value: str) -> str:
        domain = value.split('@')[-1]
        if domain in un_official_domain:
            raise ValueError("Not official Email")
        return value

class OTPVerification(BaseModel):
    email: EmailStr
    otp: str
    



def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))


def send_email(email: str, otp: str):
    
    print(f"Sending OTP {otp} to {email}")


@app.post('/userverification')
def user_verification(user: UserVerificationBase):
    email = user.email
    otp = generate_otp()
    otp_storage[email] = otp
    send_email(email, otp)
    return {"message": "OTP sent to your email"}



@app.post('/verify-otp')
def verify_otp(verification: OTPVerification):
    stored_otp = otp_storage.get(verification.email)
    if stored_otp and stored_otp == verification.otp:
        return {"message": "OTP verified successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid OTP")


@app.post('/clear-otp')
def clear_otp(email: EmailStr):
    otp_storage.pop(email, None)
    return {"message": "OTP cleared"}
