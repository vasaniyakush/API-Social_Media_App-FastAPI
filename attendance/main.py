from cgitb import html
import codecs
from pydoc import render_doc
from urllib import request
from fastapi import FastAPI,Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

class Id(BaseModel):
    id:str
app = FastAPI()

@app.get("/",response_class=HTMLResponse)
def read_items():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        <form action="/" method="post">
            <input type="text" name="id" id="id">
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """

@app.post("/",response_class=HTMLResponse)
def addattendance(id:str = Form()):
    print(id)
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        Form Successfully Submited
        <form action="/" method="post">
            <input type="text" name="id" id="id">
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """
    
