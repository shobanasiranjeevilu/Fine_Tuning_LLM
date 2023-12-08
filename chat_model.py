from openai import OpenAI
import nbformat
import json


class API():
    def __init__(self, api_key) -> None:
        self.client = OpenAI(api_key=api_key)
        

    def read_notebook(self, content):
        return nbformat.read(content, as_version=4)

    def extract_cells(self, notebook):
        cells = []
        for cell in notebook.cells:
            if cell.cell_type in ['markdown', 'code']:
                cells.append({
                    'type': cell.cell_type,
                    'content': cell.source
                })
        return cells

    def format_for_gpt(self, cells):
        formatted_data = {
            "cells": cells
        }
        return json.dumps(formatted_data, separators=(',', ':'))

    def load_examples(self):
        # Example 1
        notebook = self.read_notebook("/Users/shobanasiranjeevilu/Downloads/sample_work/sample_work/sample_assignments/assignment_3.ipynb")
        extracted_cells = self.extract_cells(notebook)
        self.example_1 = self.format_for_gpt(extracted_cells)

        # Example 2
        notebook = self.read_notebook("/Users/shobanasiranjeevilu/Downloads/sample_work/sample_work/sample_assignments/assignment_2.ipynb")
        extracted_cells = self.extract_cells(notebook)
        self.example_2 = self.format_for_gpt(extracted_cells)

        # Example 3
        notebook = self.read_notebook("/Users/shobanasiranjeevilu/Downloads/sample_work/sample_work/sample_assignments/assignment_7.ipynb")
        extracted_cells = self.extract_cells(notebook)
        self.example_3 = self.format_for_gpt(extracted_cells)

    def api_model(self,input_submission,context):

      self.load_examples()

      system_content = "You are a helpful assistant that evaluate programming assignments and check all the instructions are followed and grade it from 1-100 and provide Feedback what went wrong.Provide Reasoning on why you gave such grade. " + context

      messages=[
          {
            "role": "system",
            "content": "You are a helpful assistant that evaluate python program and grad from 1-100 and explain why you gave such grade. make sure to provide your response in bullet points\
                      Write three Python scripts using mrjob that tell me:\
              Average number of words in each review (define “words” however you like but be explicit about it)\
              Count of reviews by year-month (eg “2021-09”)\
              Average rating of any review marked ”cool” (eg where cool != 0)"
          },
          {
            "role": "user",
            "content": self.example_1
          },
          {
            "role": "assistant",
            "content": "Grade:85, summarized Feedback: Question2 is not executable, Question3 gives no output. Add notebook with executed output/ output files next time, Possible Errors: None"
          },
          {
            "role": "user",
            "content": self.example_2
          },
          {
            "role": "assistant",
            "content": "Grade:85, summarized Feedback: Question 1 will not execute, Possible Errors: Incorrect class name is used while invoking"
          },
          {
            "role": "user",
            "content": self.example_3
          },
          {
            "role": "assistant",
            "content":  "Grade:20, summarized Feedback: Doesn't follow the instruction. No map/reduce logic has been written to do the task. DataFrames are not allowed"
          },
          {
              "role": "system",
              "content": system_content
          },
          {
              "role": "user",
              "content": input_submission 
          }
          
        ]
        
      response = self.client.chat.completions.create(
        model="gpt-4",
        messages= messages,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
      )
      return response.choices[0].message.content



