from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
import json
import requests
import cgi
import sqlite3
import os,glob
app=Flask(__name__)

@app.route('/')
def home():
    form='<form name="form1" method="POST" action="result1" enctype="multipart/form-data">\n'
    form=form+'<input type="file" name="files">\n'
    form=form+'<input type="submit" value="送信">\n</form>\n<br>\n'
    form=form+'<form name="form1" method="POST" action="result2">\n'
    form=form+'<input type="text" name="name">'
    form=form+'<textarea name="cont" rows="4" cols="40"></textarea>'
    form=form+'<input type="submit" value="送信">\n</form>\n<br>'
    return form

@app.route('/result1',methods=['POST','GET'])
def result1():
    try:       
        item=request.files["files"]
        item.save(item.filename)
    except:
        a=1
    output=""
    for path in glob.glob("*"):
        output=output+"<a href=\"http://localhost:5000/file/"+path+"\">"+path+"</a><br>\n"
    return output

@app.route('/result2',methods=['POST','GET'])
def result2():
    try:       
        name=request.form["name"]
        cont=request.form["cont"]
        with open(name+".txt", mode='w',encoding="utf-8") as f:
            f.write(cont)
            f.close
    except:
        a=1
    output=""
    for path in glob.glob("*"):
        output=output+"<a href=\"http://localhost:5000/file/"+path+"\">"+path+"</a><br>\n"
    return output

@app.route('/file/<name>')
def FILE(name):
    f=open(name,"r")
    s=f.read()
    resp=Response(s)
    return resp
    
if __name__=='__main__':
    app.run(host='0.0.0.0')
