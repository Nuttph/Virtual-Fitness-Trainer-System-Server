from fastapi import APIRouter,Depends,HTTPException
from schemas.exercise import ExerciseRelation, ExerciseRelationUpdate
from database import get_connection
from auth import get_current_user

router = APIRouter()

@router.get("/")
async def read_foods(current_user:dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("EXEC sp_get_foods")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    result = [] 
    for row in data:
        result.append({
            'food_id':row[0],
            'food_name': row[1],
            'calories': row[2],
            'unit': row[3]
        })
    return result