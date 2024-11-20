
import json
from flask import Flask,request, jsonify, json   #,make_response
import datetime
from datetime import datetime

app = Flask(__name__)

with open("showInfoSmall.json", "r", encoding="utf-8") as fp:
    info = json.load(fp)
with open("seasonSmall.json", "r", encoding="utf-8") as fp:
    shows = json.load(fp)
with open("namesToId.json", "r", encoding="utf-8") as fp:
    names = json.load(fp)
nameLst=[]
idLst=[]
for i in names.keys():
    nameLst.append(i)
    idLst.append(names[i])
namesId={
    "id":idLst,
    "titles":nameLst
}

@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
        print(names.keys())
  
        data = "hello world"
        return jsonify({'data': namesId})
    
@app.route('/id/<string:show>', methods = ['GET'])
def showId(show):
    showInfo={}
    try:
        temp=show.replace("_"," ")
        showInfo["id"]=names[temp]
    except SyntaxError:
        print(show)
  
    return jsonify({'data': showInfo})
  
@app.route('/details/<string:id>', methods = ['GET']) #name, image, synopsis, air date
def showDetails(id):
    showInfo={}
    try:
        print(info[id])
        showInfo["title"]=info[id]["title"]
        showInfo["image"]=info[id]["main_picture"]["medium"]
        showInfo["broadcast"]=info[id]["broadcast"]["day_of_the_week"]

        #gist=info[id]["synopsis"]
    except:
        return jsonify({'data': "id was malformed or does not exist"})

  
    return jsonify({'data': showInfo})
#23539

#https://api.myanimelist.net/v2/anime/season/{year}/{season}
@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
        print(names.keys())
  
        data = "hello world"
        return jsonify({'data': namesId})

if __name__ == '__main__':
    app.run(debug = True)

