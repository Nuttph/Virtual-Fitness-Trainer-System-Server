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
