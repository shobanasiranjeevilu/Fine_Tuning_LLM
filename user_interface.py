import nbformat
import json
import io
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import nbformat
from Submission.chat_model import API


app = FastAPI()

def read_notebook(content):
    return nbformat.read(content, as_version=4)

def extract_cells(notebook):
    cells = []
    for cell in notebook.cells:
        if cell.cell_type in ['markdown', 'code']:
            cells.append({
                'type': cell.cell_type,
                'content': cell.source
            })
    return cells
def format_for_gpt(cells):
    formatted_data = {
        "cells": cells
    }
    return json.dumps(formatted_data, separators=(',', ':'))


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
    
    notebook = read_notebook(io.BytesIO(content))
    extracted_cells = extract_cells(notebook)
    formatted_data = format_for_gpt(extracted_cells)
    api = API(api_key="")
    response = api.api_model(formatted_data,instructions)

    response = response.split("\n")

    return response
