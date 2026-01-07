from pydantic import BaseModel
from typing import Optional

class Student(BaseModel):
    roll_no: int
    name: str
    age: int
    department: str
    cgpa: float

class UpdateStudent(BaseModel):
    name: Optional[str]
    age: Optional[int]
    department: Optional[str]
    cgpa: Optional[float]
