from fastapi import FastAPI 
from routers.student_router import router

app = FastAPI()

app.include_router(router)