from fastapi import FastAPI, File, UploadFile, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import test_rag as tst

load_dotenv()

app = FastAPI()

# Mount static files (for uploaded PDFs, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Google Sheets Authentication
# def authenticate_google_sheets():
#     scope = [
#         "https://spreadsheets.google.com/feeds",
#         "https://www.googleapis.com/auth/spreadsheets",
#         "https://www.googleapis.com/auth/drive.file",
#         "https://www.googleapis.com/auth/drive"
#     ]
#     creds = ServiceAccountCredentials.from_json_keyfile_name(
#         r"C:\\Users\\lalpa\\Documents\\soft_fl\\flasktest101-c9059b332632.json", scope
#     )
#     client = gspread.authorize(creds)
#     return client
# file_path = None
# flag = 0

# Form Submission Model
class ContactForm(BaseModel):
    name: str
    email: str
    message: str

@app.get("/", response_class=HTMLResponse)
def root():
    return "<h1>Welcome to FastAPI</h1>"

@app.post("/submit")
def submit(form: ContactForm):
    client = authenticate_google_sheets()
    try:
        sheet = client.open("flask_test_101").sheet1  # Update with actual spreadsheet name
        sheet.append_row([form.name, form.email, form.message])
        return JSONResponse(content={"message": "Data submitted successfully"})
    except gspread.SpreadsheetNotFound:
        return JSONResponse(content={"error": "Spreadsheet not found. Check permissions."}, status_code=404)

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    global file_path, flag
    file_location = f"static/uploads/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())
    file_path = file_location
    flag = 1
    return JSONResponse(content={"message": f"File '{file.filename}' uploaded successfully!"})

@app.post("/chat")
def chat(user_message: str = Form(...)):
    global file_path, flag
    if flag == 0:
        file_path = r'C:/Users/lalpa/Documents/soft_fl/static/uploads/test_file.pdf'
    response = tst.input(file_path, user_message)
    return JSONResponse(content={"response": response})
