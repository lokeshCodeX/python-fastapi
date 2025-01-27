from fastapi import FastAPI, HTTPException
import uvicorn
import mysql.connector
from mysql.connector import Error

app = FastAPI()


# MySQL connection setup
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',  # Your MySQL host
        user='root',       # Your MySQL user
        password='admin@123',  # Your MySQL password
        database='lokesh'  # Your database name
    )

@app.get("/")
def hello():
    print("hello")
    return "hello world"

@app.put("/listing")
def get_students():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()
        return result
    except Error as e:
        raise HTTPException(status_code=500, detail="Database connection failed")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.get("/rigester")
def add_student(userName: str, rollno: str):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (userName, rollno) VALUES (%s, %s)", (userName, rollno))
        connection.commit()
        return {"message": "Student added successfully", "userName": userName, "rollno": rollno}
    except Error as e:
        raise HTTPException(status_code=500, detail="Failed to add student")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.get("/gettodos/{id}")
def get_todos(id: int):
    print("this is print statement!")
    return {"message": "this is gettodos", "output": id}

@app.get("/getsingle")
def get_single(userName: str, rollno: str):
    print("hello Lokesh, this is single todo", userName, rollno)
    return "hello single todo"

def start():
    uvicorn.run("todos.main:app", host="127.0.0.1", port=8080)
