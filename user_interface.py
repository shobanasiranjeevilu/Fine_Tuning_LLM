import nbformat
import json
import io
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import nbformat
from chat_model import API
from utils import read_content, extract_cells, format_for_gpt




app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), instructions: str = Form(...)):
    # Validate the file type
    if not file.filename.endswith(('.ipynb', '.pdf')):
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Read the content of the file
    content = await file.read()
    response = process_file(content, instructions)

    return {"filename": file.filename, 'Evaluation': response}



def process_file(content,instructions):
    
    notebook = read_content(io.BytesIO(content))
    extracted_cells = extract_cells(notebook)
    formatted_data = format_for_gpt(extracted_cells)
    api = API(api_key="")
    response = api.api_model(formatted_data,instructions)

    response = response.split("\n")

    return response
