from flask import Flask
from flask import jsonify
import json
import requests
app=Flask(__name__)

@app.route('/<word>')
def MSU(word):
    url="http://ja.dbpedia.org/data/"+word+".json"
    res=requests.get(url)
    res.raise_for_status()
    jsn=json.loads(res.text)
    abstract=jsn["http://ja.dbpedia.org/resource/"+word]["http://dbpedia.org/ontology/abstract"][0]["value"]
    try:
        thumnail=jsn["http://ja.dbpedia.org/resource/"+word]["http://dbpedia.org/ontology/thumbnail"][0]["value"]
        output="<h1>"+word+"</h1>"
        output=output+"<h2>概要</h2>"+abstract+"<br>"
        output=output+'<img src="'+thumnail+'">'
        return output
    except:
        output="<h1>"+word+"</h1>"
        output=output+"<h2>概要</h2>"+abstract+"<br>"
        return output
    
    
if __name__=='__main__':
    app.run(host='0.0.0.0')
