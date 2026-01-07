def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "roll_no": student.get("roll_no"),
        "name": student.get("name"),
        "age": student.get("age"),
        "department": student.get("department"),
        "cgpa":student.get("cgpa"),
    }
