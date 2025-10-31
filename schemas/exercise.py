from pydantic import BaseModel

class ExerciseRelation(BaseModel):
    move_id: int
    sets: int
    reps_per_set: int
    duration: int
    leftCount: int
    rightCount: int
    weight:int

class ExerciseRelationUpdate(ExerciseRelation):
    exer_id: int

class ExerciseRelationDelete(BaseModel):
    exer_id: int
    user_id: int