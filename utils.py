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


def create_prompt_example(path_to_example,human_grade,human_feedback):
    
    notebook = read_notebook(path_to_example)
    extracted_cells = extract_cells(notebook)
    parsed_example = format_for_gpt(extracted_cells)
    human_feedback_example_prompt = "Grade:{}, summarized_feedback:{}".format(human_grade,human_feedback)

    return parsed_example, human_feedback_example_prompt

