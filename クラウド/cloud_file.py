from flask import Flask
from flask import jsonify
from flask import request
import json
import requests
import cgi
import sqlite3
import os,glob
app=Flask(__name__)

@app.route('/')
def home():
    form='<form name="form1" method="POST" action="result" enctype="multipart/form-data">'
    #form=form+'<input type="text" name="user">'
    form=form+'<input type="file" name="files">'
    form=form+'<input type="submit" value="送信">'
    return form

@app.route('/result',methods=['POST','GET'])
def result():
    try:
        #user=request.form["user"]        
        item=request.files["files"]
        item.save(item.filename)
    except:
        a=1
    output=""
    #print(glob.glob("/"+user+"/*"))
    #fold="/"+user+"/"
    for path in glob.glob("*"):
        output=output+"<a href=\"http://localhost:5000/file/"+path+">"+path+"</a><br>\n"
    return output

@app.route('/file/<name>')
def FILE(name):
    f=open("/"+user+"/"+name,"r")
    s=f.read()
    resp=flask.Response(s)
    return resp
    
if __name__=='__main__':
    app.run(host='0.0.0.0')
