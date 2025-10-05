from fastapi import APIRouter,Depends,HTTPException
from schemas.exercise import ExerciseRelation
from database import get_connection
from auth import get_current_user
router = APIRouter()

@router.post("/history")
async def history(current_user:dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        select
	e.move_id,
	em.move_name,
	SUM(e.leftarm+e.rightarm) as counter,
	SUM(e.sets) as sets,
	e.reps_per_set,
	SUM(e.duration) as duration,
	CAST(e.created_at AS DATE) as date
from Exercises as e
left join ExerciseMoves as em on e.move_id = em.move_id
where e.user_id = ?
group by e.move_id,em.move_name, CAST(e.created_at AS DATE),e.reps_per_set,e.created_at
order by
	e.created_at DESC
""",current_user['user_id'])
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    result = []
    for row in data:
        result.append({
            'move_id':row[0],
            'move_name':row[1],
            'counter':row[2],
            'sets':row[3],
            'reps':row[4],
            'duration':row[5],
            'date':row[6]
        })
    return result

@router.post("/move-dashboard")
async def dashboard(current_users:dict = Depends(get_current_user)):
    conn = get_connection();
    cursor = conn.cursor();
    cursor.execute("""
            select e.move_id,em.move_name,SUM(e.leftarm+e.rightarm) as counter from Exercises as e
  left join ExerciseMoves as em on e.move_id = em.move_id
  where e.user_id = ?
  group by e.move_id,em.move_name
""",current_users['user_id'])
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    print(f'data {data}')
    result = []
    for row in data:
        result.append({
            "id":row[0],
            "title":row[1],
            "counter":row[2]
        })
    return result

@router.post("/move-save")
async def exercise_save(move_data: ExerciseRelation ,current_users:dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(" EXEC sp_add_exercise ?, ?, ?, ?, ?, ?, ?; ",
                   (
                       current_users['user_id'],
                       move_data.move_id,
                       move_data.sets,
                       move_data.reps_per_set,
                       move_data.duration,
                       move_data.leftCount,
                       move_data.rightCount
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