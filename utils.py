import nbformat
import json

def read_notebook(notebook_path):
        with open(notebook_path, 'r', encoding='utf-8') as f:
            return nbformat.read(f, as_version=4)
        

def read_content(content):
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



