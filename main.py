from fastapi import FastAPI
from routers import exercise, users,foods
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(exercise.router, prefix="/exercise", tags=["exercise"])
app.include_router(foods.router, prefix="/foods", tags=["foods"])