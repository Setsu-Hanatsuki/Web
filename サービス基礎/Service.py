from flask import Flask
from flask import jsonify
import json
import requests
import csv
app=Flask(__name__)

@app.route('/')
def HOMT():
    f=open('KEN_ALL_ROME.CSV','r',encoding='shift-jis')
    reader=csv.reader(f)
    header=next(reader)
    out=""
    tmp="a"
    for row in reader:
        if tmp!=row[1]:
            out=out+'<a href="http://localhost:5000/state/'+row[4]+'">'+row[1]+"</a><br>\n"
            tmp=row[1]
    return out

@app.route('/city/<city>')
def CITY(city):
    f=open('KEN_ALL_ROME.CSV','r',encoding='shift-jis')
    reader=csv.reader(f)
    header=next(reader)
    out="<table>\n"
    for row in reader:
        if row[5]==city:
            out=out+"<tr><td>"+row[3]+"</td><td>"+row[0]+"</td></tr>\n"
    out=out+"</table>"
    return out

@app.route('/state/<state>')
def STATE(state):
    f=open('KEN_ALL_ROME.CSV','r',encoding='shift-jis')
    reader=csv.reader(f)
    header=next(reader)
    out=""
    tmp="a"
    for row in reader:
        if row[4]==state:
            if tmp!=row[2]:
                out=out+'<a href="http://localhost:5000/city/'+row[5]+'">'+row[2]+"</a><br>\n"
                tmp=row[2]
    return out

if __name__=='__main__':
    app.run(host='0.0.0.0')
