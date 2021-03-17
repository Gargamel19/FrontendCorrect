import json
import os

from flask import render_template, redirect, url_for, request
from app import app
import requests
import configparser

config = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
path_config = os.path.join(dir_path, ".config")
config.read(path_config)
port = config['BACKEND']['port']
beckend_endpoint = config['BACKEND']['ip']
print(type(port))
if port != "80":
    beckend_endpoint = beckend_endpoint + ":" + port

selected = ""


@app.route('/', methods=['GET'])
def ueberlieferung():
    response = requests.get(beckend_endpoint + "/sammlungen")
    files = json.loads(response.text)
    return render_template('index.html', title='Home', files=files, url=request.url)


@app.route('/sammlung/<name>', methods=['GET'])
def sammlung(name):
    response = requests.get(beckend_endpoint + "/sammlung/" + name)
    files = json.loads(response.text)
    return render_template('index_ueberlieferung.html', title='Home', files=files, url=request.url)


@app.route('/sammlung/<name>/text/<text>', methods=['GET'])
def sammlung_text(name, text):
    response = requests.get(beckend_endpoint + "/sammlung/{}/text/{}".format(name, text))
    files = json.loads(response.text)
    return_list = []
    for form in files:
        return_list.append([form[0], form[1]])
    return render_template('index_ueberlieferung_text.html', title='Home', files=return_list, url=request.url,
                           len=len(return_list))


@app.route('/sammlung/<name>/text/<text>', methods=['POST'])
def sammlung_text_post(name, text):
    erg = []
    for key in request.form.keys():
        if str(key).startswith("cat_"):
            erg.append([[], request.form.get(key)])
        elif str(key).startswith("wordContainer_"):
            if len(erg) == 0:
                erg.append([[], "nosegment"])
            erg[len(erg)-1][0].append(request.form.get(key))
    url = beckend_endpoint + "/sammlung/{}/text/{}".format(name, text)
    print(json.dumps(erg))
    requests.post(url, json=json.dumps(erg))
    return redirect(url_for("sammlung_text", name=name, text=text))
