from flask import Flask
from flask import jsonify
from flask import request
import json
import requests
import cgi
import sqlite3
app=Flask(__name__)

@app.route('/')
def home():
    #form='<form name="form1" method="POST" action="result" enctype="multipart/form-data">'
    #form=form+'<input type="file" name="files">'
    #
    #form=form+'<input type="submit" value="送信">'
    form='<br><a href="http://localhost:5000/chat">login</a>'
    return form

@app.route('/result',methods=['POST','GET'])
def result():
    if request.method == "POST":
        #form = cgi.FieldStorage()
        #if form.has_key('filename'):
        item=request.files["files"]
        #item=request.args.get('file')
        print(item)
        item.save(item.filename)
        #print(item)
        #print(app.config['UPLOAD_FOLDER'])
        return "hello"
"""
@app.route('/chat')
def chat():
    DBname="pass.db"
    form='<form name="form1" method="POST" action="chat1">'
    form=form+'<input type="text" name="ID"><br>'
    form=form+'<input type="text" name="content">'
    form=form+'<input type="submit" value="送信"><br>'
    con=sqlite3.connect(DBname)
    #print("OK")
    cur=con.cursor()
    print("OK")
    SQL="select*from post"
    for row in cur.execute(SQL):
        form="<br>"+form+"name:"+row[0]+"<br>"+row[1]+"<br>"
    cur.close()
    con.close()
    return form
"""
@app.route('/chat',methods=['POST','GET'])
def chat():
    DBname="pass.db"
    con=sqlite3.connect(DBname)
    cur=con.cursor()
    try:
        ID=request.form["ID"]
        content=request.form["content"]
        cur.execute("insert into post values('%s','%s')"%(ID,content))
        con.commit()
    except:
        a=1
    #cur.close()
    #con.close()
    form='<form name="form1" method="POST" action="chat">'
    form=form+'<input type="text" name="ID"><br>'
    form=form+'<input type="text" name="content">'
    form=form+'<input type="submit" value="送信"><br>'
    #con=sqlite3.connect(DBname)
    #print("OK")
    #cur=con.cursor()
    #print("OK")
    SQL="select*from post"
    for row in cur.execute(SQL):
        form="<br>\n"+form+"name:"+row[0]+"<br>\n"+row[1]+"<br>\n"
    cur.close()
    con.close()
    return form
    
    
if __name__=='__main__':
    app.run(host='0.0.0.0')
