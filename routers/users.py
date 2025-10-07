from fastapi import APIRouter,HTTPException, Form,Depends
from database import get_connection
from schemas.users import UserRegister,UserEdit
# import hashlib
import bcrypt
from jose import jwt
import secrets
from datetime import datetime,timedelta,timezone
import os
from dotenv import load_dotenv
from auth import get_current_user

router = APIRouter()
load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGO = os.getenv('JWT_ALGO')
OUR_ACCESS_EXPIRES_MINUTES = os.getenv('OUR_ACCESS_EXPIRES_MINUTES')
OUR_REFRESH_EXPIRES_DAYS = os.getenv('OUR_REFRESH_EXPIRES_DAYS')


@router.post("/login")
async def login_user(email: str = Form(...), password: str = Form(...)):
    conn = get_connection()
    cursor = conn.cursor()

    # ดึง user จากฐานข้อมูล
    cursor.execute("SELECT user_id, password FROM Users WHERE email = ?", (email,))
    row = cursor.fetchone()

    if not row:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Invalid email or password")

    user_id, hashed_password = row[0], row[1]
    
    # เช็ครหัสผ่านด้วย bcrypt
    if not bcrypt.checkpw(password.encode(), hashed_password.encode()):
        cursor.close()
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    now = datetime.now(timezone.utc)

    # สร้าง access token
    access_payload = {
        "sub": str(user_id),
        "exp": int((now + timedelta(minutes=int(OUR_ACCESS_EXPIRES_MINUTES))).timestamp())
    }
    access_token = jwt.encode(access_payload, JWT_SECRET, algorithm=JWT_ALGO)

    # สร้าง refresh token
    refresh_token = secrets.token_urlsafe(64)
    refresh_expires = now + timedelta(days=int(OUR_REFRESH_EXPIRES_DAYS))

    cursor.execute(
        "INSERT INTO UserToken (user_id, token, type, expires_at) VALUES (?, ?, 'refresh', ?)",
        (user_id, refresh_token, refresh_expires)
    )
    conn.commit()
    cursor.close()
    conn.close()

    # return token
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": int(OUR_ACCESS_EXPIRES_MINUTES) * 60
    }

@router.post("/register")
async def register_user(user: UserRegister):
    conn = get_connection()
    cursor = conn.cursor()
    

    cursor.execute("""
                   select user_id from Users where email = ?
                   """,(user.email))
    exiting_user = cursor.fetchone()
    if exiting_user:
        cursor.close()
        conn.close()
        # return {"message": "User already exists"}
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hased_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    hased_password_str = hased_password.decode();

    cursor.execute("""
                INSERT INTO Users (firstname, lastname, email, password, img, birthdate, weight, height, gender)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                   """,
                   (user.firstname, user.lastname, user.email, hased_password_str, user.img, user.birthdate, user.weight, user.height,user.gender)
                     )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "User registered successfully"}
   

@router.get('/profile')
async def profile_user(current_user: dict = Depends(get_current_user)):
    conn = get_connection();
    cursor = conn.cursor();
    cursor.execute("""
        select 
            u.firstname,u.lastname,u.email,u.birthdate,u.gender,u.weight,u.height
        from users as u
        where u.user_id = ?
""",(current_user['user_id']))
    data = cursor.fetchone();
    # print(f'current_user = {data}')
    gender = "None"
    if(int(data[4]) == 1):
        gender = "Man"
    elif(int(data[4]) == 2):
        gender = "Woman"

    return {
        "firstname":data[0],
        "lastname":data[1],
        "email":data[2],
        "dob":data[3],
        "gender":gender,
        "weight":data[5],
        "height":data[6]
    }

@router.post('/edit')
async def edit_profile(newData:UserEdit,current_user:dict = Depends(get_current_user)):
    print(current_user['user_id'])
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password from Users where user_id = ?",current_user['user_id'])
    password = cursor.fetchone()
    print(password[0])
    print(newData.password.encode())
    checkPassword = bcrypt.checkpw(newData.password.encode(),password[0].encode())
    print(f'check password {checkPassword}')
    if(not checkPassword):
        cursor.close()
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    cursor.execute("""
                    UPDATE Users
                    SET firstname = ? ,lastname = ? ,birthdate = ?, weight = ?, height = ?, gender = ?
                    where user_id = ? ;
                    """,newData.firstname,newData.lastname,newData.brithdate,newData.weight,newData.height,newData.gender,current_user['user_id'])
    cursor.commit()
    cursor.close()
    conn.close()

    return {
        "message":"update sucess"
    }