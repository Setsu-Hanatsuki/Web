from flask import Flask
from flask import jsonify
import json
import requests
import csv
app=Flask(__name__)

@app.route('/city/<city>')
def CITY(city):
    f=open('KEN_ALL_ROME.CSV','r',encoding='shift-jis')
    reader=csv.reader(f)
    header=next(reader)
    jsn={}
    for row in reader:
        if row[5]==city:
            jsn[row[3]]=row[0]
    return jsonify(jsn)

@app.route('/state/<state>')
def STATE(state):
    f=open('KEN_ALL_ROME.CSV','r',encoding='shift-jis')
    reader=csv.reader(f)
    header=next(reader)
    jsn={}
    for row in reader:
        if row[4]==state:
            jsn[row[3]]=row[0]
    return jsonify(jsn)
    
    
if __name__=='__main__':
    app.run(host='0.0.0.0')
