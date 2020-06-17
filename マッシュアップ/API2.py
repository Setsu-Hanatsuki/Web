from flask import Flask
from flask import jsonify
import json
import requests
app=Flask(__name__)

@app.route('/<word>')
def MSU(word):
    url="http://geoapi.heartrails.com/api/json?method=searchByPostal&postal="+word
    res=requests.get(url)
    res.raise_for_status()
    jsn=json.loads(res.text)
    ido=jsn["response"]["location"][0]["y"]
    keido=jsn["response"]["location"][0]["x"]
    city=jsn["response"]["location"][0]["city"]
    town=jsn["response"]["location"][0]["town"]
    output="<h1>"+word+"</h1>"
    output=output+"<h2>"+city+town+"</h2>"
    chizu="<script type='text/javascript' charset='UTF-8' src='https://map.yahooapis.jp/MapsService/embedmap/V2/?cond=compress%3A-0%3Blabels%3A%2C%3Bfit%3Atrue%3Btraffic%3Atrain%3Bwalkspd%3A4.8%3Bws%3A3%3Bptn%3Ase%2Cex%2Cal%2Chb%2Clb%2Csr%3B&amp;zoom=18&amp;bbox=141.3507104102472%2C43.07270910421585%2C141.35532380975286%2C43.07426870353261&amp;lat="+ido+"&amp;lon="+keido+"&amp;pluginid=my&amp;z=19&amp;mode=map&amp;active=true&amp;layer=my&amp;home=off&amp;pointer=off&amp;pan=off&amp;ei=utf8&amp;v=3&amp;datum=wgs&amp;width=480&amp;height=360&amp;device=pc&amp;isleft='></script>"
    output=output+chizu
    return output
    
    
if __name__=='__main__':
    app.run(host='0.0.0.0')
