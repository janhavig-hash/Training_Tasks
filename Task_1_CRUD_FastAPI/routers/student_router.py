from fastapi import APIRouter, HTTPException
from database import student_collection
from schemas import Student, UpdateStudent
from models import student_helper

router = APIRouter()

# CREATE STUDENT
@router.post("/students")
def create_student(student: Student):
    if student_collection.find_one({"roll_no": student.roll_no}):
        raise HTTPException(status_code=400, detail="Roll number already exists")

    result = student_collection.insert_one(student.dict())
    new_student = student_collection.find_one({"_id": result.inserted_id})
    return student_helper(new_student)


# READ ALL STUDENTS
@router.get("/students")
def get_all_students():
    students = []
    for student in student_collection.find():
        students.append(student_helper(student))
    return students


# READ STUDENT BY ROLL NO
@router.get("/students/{roll_no}")
def get_student_by_roll(roll_no: int):
    student = student_collection.find_one({"roll_no": roll_no})
    if student:
        return student_helper(student)
    raise HTTPException(status_code=404, detail="Student not found")


# UPDATE STUDENT BY ROLL NO
@router.put("/students/{roll_no}")
def update_student_by_roll(roll_no: int, student: UpdateStudent):
    updated_data = {k: v for k, v in student.dict().items() if v is not None}

    if len(updated_data) == 0:
        raise HTTPException(status_code=400, detail="No data provided")

    result = student_collection.update_one(
        {"roll_no": roll_no},
        {"$set": updated_data}
    )

    if result.matched_count == 1:
        updated_student = student_collection.find_one({"roll_no": roll_no})
        return student_helper(updated_student)

    raise HTTPException(status_code=404, detail="Student not found")


# DELETE STUDENT BY ROLL NO
@router.delete("/students/{roll_no}")
def delete_student_by_roll(roll_no: int):
    result = student_collection.delete_one({"roll_no": roll_no})

    if result.deleted_count == 1:
        return {"message": "Student deleted successfully!"}

    raise HTTPException(status_code=404, detail="Student not found")
