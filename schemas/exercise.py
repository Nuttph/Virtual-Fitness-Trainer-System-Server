from pydantic import BaseModel

class ExerciseRelation(BaseModel):
    move_id: int
    sets: int
    reps_per_set: int