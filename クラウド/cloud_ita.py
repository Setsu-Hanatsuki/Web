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
    form='<br><a href="http://localhost:5000/chat">login</a>'
    return form

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
    form='<form name="form1" method="POST" action="chat">'
    form=form+'<input type="text" name="ID"><br>'
    form=form+'<input type="text" name="content">'
    form=form+'<input type="submit" value="送信"><br>'
    SQL="select*from post"
    for row in cur.execute(SQL):
        form=form+"name:"+row[0]+"<br>\n"+row[1]+"<br>\n"
    cur.close()
    con.close()
    return form
    
if __name__=='__main__':
    app.run(host='0.0.0.0')
