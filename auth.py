# auth.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# โหลดค่า .env
load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET", "supersecret")
JWT_ALGO = os.getenv("JWT_ALGO", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # กำหนดเวลา token หมดอายุ (นาที)

# OAuth2PasswordBearer สำหรับดึง token จาก header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


# ฟังก์ชันสร้าง access token
def create_access_token(user_id: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": user_id,
        "exp": int(expire.timestamp())
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)
    return token


# ฟังก์ชันตรวจสอบ token (ใช้ Depends ใน route)
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        print("Received token:", token)
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        print("Decoded payload:", payload)

        user_id = payload.get("sub")
        exp = payload.get("exp")
        print("Current UTC timestamp:", datetime.utcnow().timestamp())

        if user_id is None:
            raise HTTPException(status_code=401, detail="User ID missing in token")
        if exp < datetime.utcnow().timestamp():
            raise HTTPException(status_code=401, detail="Token expired")

    except JWTError as e:
        print("JWT decode error:", e)
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"user_id": user_id}
