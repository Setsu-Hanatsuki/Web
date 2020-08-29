from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask import send_file
from flask import render_template
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz
import numpy as np
import json
import requests
import cgi
import sqlite3
import os,glob
import csv
import subprocess
#app=Flask(__name__,static_url_path='/static')
app=Flask(__name__)
def rcsv(file):
    f=open(file,"r")
    reader=csv.reader(f)
    k=0
    name=[]
    tmp=[]
    x=[]
    y=[]
    for row in reader:
        if k==0:
            for j in range(len(row)):
                if j!=0:
                    name.append(row[j])
            k=1
        else:
            for i in range(len(row)):
                if i!=0:
                    tmp.append(row[i])
                else:
                    y.append(int(row[i]))
            x.append(tmp)
            tmp=[]
    return x,y,name
    
def graph(file):
    x,y,name=rcsv(file)
    #x = preprocessing.minmax_scale(x)
    clf = DecisionTreeClassifier(max_depth=10)
    clf.fit(x, y)
    cn={}
    for i in range(len(y)):
        y[i]=str(y[i])
        try:
            a=cn[y[i]]
        except:
            cn[y[i]]=1
    class_names=[]
    for key in cn:
        class_names.append(key)
    export_graphviz(clf, "tree1.1.dot",feature_names=name,class_names=class_names,filled=True,proportion=True)
    
    subprocess.run("dot -Tpng tree1.1.dot -o static/images/graph1.png".split())
    a=1
    
    return a
    
def rf(file):
    x,y,name=rcsv(file)
    x = preprocessing.minmax_scale(x)
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(x, y)
    importances = clf.feature_importances_
    out=[]
    tmp=[]
    for i in range(len(x[0])):
        tmp.append(name[i])
        tmp.append(importances[i])
        out.append(tmp)
        tmp=[]
    return out
    
def reg(file):
    f=open(file,"r")
    reader=csv.reader(f)
    k=0
    name=[]
    tmp=[]
    x=[]
    y=[]
    for row in reader:
        if k==0:
            for j in range(len(row)):
                if j!=0:
                    name.append(row[j])
            k=1
        else:
            for i in range(len(row)):
                if i!=0:
                    tmp.append(float(row[i]))
                else:
                    y.append(float(row[i]))
            x.append(tmp)
            tmp=[]
    reg = linear_model.LinearRegression()
    reg.fit(x, y)
    x=np.array(x)
    y_pred=reg.predict(x)
    sse=np.sum((y-y_pred)**2,axis=0)
    sse=sse/(x.shape[0]-x.shape[1]-1)
    s=np.linalg.inv(np.dot(x.T,x))
    std_err=np.sqrt(np.diagonal(sse*s))
    a = reg.coef_
    b = reg.intercept_
    out=[]
    tmp=[]
    for i in range(len(name)):
        tmp.append(name[i])
        tmp.append(a[i])
        tmp.append(a[i]/std_err[i])
        out.append(tmp)
        tmp=[]
    tmp.append("切片")
    tmp.append(b)
    out.append(tmp)
    tmp=[]
    tmp.append("決定係数")
    tmp.append(reg.score(x,y))
    out.append(tmp)
    return out

@app.route('/')
def home():
    form='<h1>要因分析</h1><br>\n<h2>目的変数が連続的な場合の重要度</h2><br>\n<form name="form1" method="POST" action="result1" enctype="multipart/form-data">\n'
    form=form+'<input type="file" name="files">\n'
    form=form+'<input type="submit" value="送信">\n</form>\n<br>\n'
    form=form+'<h2>目的変数がカテゴリの場合の重要度</h2><br>\n<form name="form1" method="POST" action="result2" enctype="multipart/form-data">\n'
    form=form+'<input type="file" name="files">\n'
    form=form+'<input type="submit" value="送信">\n</form>\n<br>\n'
    form=form+'<h2>CHAID分析</h2><br>\n<form name="form1" method="POST" action="result3" enctype="multipart/form-data">\n'
    form=form+'<input type="file" name="files">\n'
    form=form+'<input type="submit" value="送信">\n</form>\n<br>\n'
    form=form+'<h2>数量化</h2><br>\n<form name="form1" method="POST" action="result4" enctype="multipart/form-data">\n'
    form=form+'<h3>項目</h3><input type="text" name="content"><br><input type="file" name="files">\n'
    form=form+'<input type="submit" value="送信">\n</form>\n<br>\n'
    return form

@app.route('/result1',methods=['POST','GET'])
def result1():
    try:        
        item=request.files["files"]
        print(item)
        item.save(item.filename)
    except:
        a=1
    file=item.filename
    out=reg(file)
    print(out)
    output="<table>\n<tr><td>項目</td><td>ウェイト</td><td>重要度</td></tr>\n"
    for i in range(len(out)):
        if i<len(out)-2:
            output=output+"<tr><td>"+str(out[i][0])+"</td><td>"+str(out[i][1])+"</td><td>"+str(out[i][2])+"</td></tr>\n"
        else:
            output=output+"<tr><td>"+str(out[i][0])+"</td><td>"+str(out[i][1])+"</td></tr>\n"
    return output

@app.route('/result2',methods=['POST','GET'])
def result2():
    try:        
        item=request.files["files"]
        print(item)
        item.save(item.filename)
    except:
        a=1
    file=item.filename
    out=rf(file)
    output="<table>\n<tr><td>項目</td><td>重要度</td></tr>\n"
    for i in range(len(out)):
        output=output+"<tr><td>"+str(out[i][0])+"</td><td>"+str(out[i][1])+"</td></tr>\n"
    return output

@app.route('/result3',methods=['POST','GET'])
def result3():
    import datetime
    dt_now = datetime.datetime.now()
    try:        
        item=request.files["files"]
        print(item)
        item.save(item.filename)
    except:
        a=1
    file=item.filename
    a=graph(file)
    return render_template("index.html",time=dt_now)

@app.route('/result4',methods=['POST','GET'])
def result4():
    import pandas as pd
    try:        
        item=request.files["files"]
        content=request.form["content"]
        print(item)
        item.save(item.filename)
    except:
        a=1
    df=pd.read_csv(item.filename,encoding="shift-jis")
    con=content.split()
    x=pd.get_dummies(df[con])
    df=pd.concat([df,x],axis=1,join='inner')
    #df.drop(df.index[[0]])
    for i in range(len(con)):
        df=df.drop(con[i],axis=1)
    df.to_csv(item.filename,encoding="shift-jis",index=False)
    with open(item.filename,"r")as f:
        a=f.read()
        f.close()
    a=a.strip('\"')
    with open("fix"+item.filename,"w")as f:
        f.write(a)
        f.close()
    return '<a href="http://localhost:5000/file/'+item.filename+'">Download</a>'
    
@app.route("/file/<name>")
def file(name):
    return send_file(name)

if __name__=='__main__':
    app.run(host='0.0.0.0')
