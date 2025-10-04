import pyodbc

# ตัวอย่างการเชื่อมต่อ SQL Server
def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LAPTOP-I7B70R26;"     # เปลี่ยนเป็นชื่อเครื่องหรือ IP
        "DATABASE=AI_FITNESS;"           # ชื่อ Database
        "UID=sa;"                    # ชื่อผู้ใช้
        "PWD=1234;"         # รหัสผ่าน
    )
    return conn
