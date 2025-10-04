from fastapi import APIRouter,Depends,HTTPException
from schemas.exercise import ExerciseRelation
from database import get_connection
from auth import get_current_user
router = APIRouter()

@router.post("/move_save")
async def exercise_save(move_data: ExerciseRelation ,current_users:dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(" EXEC sp_add_exercise ?, ?, ?, ?; ",
                   (
                       current_users['user_id'],
                       move_data.move_id,
                       move_data.sets,
                       move_data.reps_per_set
                    ))
    cursor.commit()
    return {
        "message":"move save!"
    }

@router.post("/move")
async def exercise_move():
    Depends(get_current_user)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
            select * from ExerciseMoves;
        """)
    rows = cursor.fetchall()
    # print(f'rows {rows}')
    result = []
    for row in rows:
        result.append({
            "move_id":row[0],
            "move_name":row[1]
        })
    cursor.close()
    conn.close()
    return result