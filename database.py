import pyodbc
import os
from dotenv import load_dotenv

# โหลดตัวแปรสภาพแวดล้อมจากไฟล์ .env
load_dotenv() 

# ดึงค่าจากตัวแปรสภาพแวดล้อม
DRIVER = os.getenv("DB_DRIVER")
SERVER = os.getenv("DB_SERVER")
DATABASE = os.getenv("DB_DATABASE")
UID = os.getenv("DB_UID")
PWD = os.getenv("DB_PWD")


def get_connection():
    """
    สร้างและส่งคืนการเชื่อมต่อ pyodbc ไปยัง SQL Server โดยใช้ข้อมูลจากไฟล์ .env
    """
    if not all([DRIVER, SERVER, DATABASE, UID, PWD]):
        raise ValueError("Missing one or more database environment variables (DRIVER, SERVER, DATABASE, UID, PWD).")
        
    connection_string = (
        f"DRIVER={DRIVER};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={UID};"
        f"PWD={PWD};"
    )
    
    try:
        conn = pyodbc.connect(connection_string)
        print("Database connection successful.")
        return conn
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database connection failed: {sqlstate}")
        # คุณอาจต้องการยกเว้น Error หรือจัดการ Error ตามลักษณะของแอปพลิเคชัน
        raise
