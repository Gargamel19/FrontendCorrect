import json
import os
from datetime import datetime

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


def get_backup_list(name, text):
    response = requests.get(beckend_endpoint + "/sammlung/{}/text/{}/backups".format(name, text))
    backups = json.loads(response.text)
    new_backups = []
    for backup in backups:
        content = backup.replace("_r_.xml", "").split("-")[1:]
        print(int(content[0]), int(content[1]), int(content[2]),int(content[3]), int(content[4]), int(content[5].split(".")[0]))
        dt = datetime(year=int(content[0]), month=int(content[1]), day=int(content[2]),
                      hour=int(content[3]), minute=int(content[4]), second=int(content[5].split(".")[0]))
        new_backups.append([backup, str(dt)])
    return new_backups

@app.route('/', methods=['GET'])
def ueberlieferung():
    response = requests.get(beckend_endpoint + "/sammlungen")
    files = json.loads(response.text)
    return render_template('index.html', title='Home', files=files, url=request.url)


@app.route('/sammlung/<name>', methods=['GET'])
def sammlung(name):
    response = requests.get(beckend_endpoint + "/sammlung/" + name)
    files = json.loads(response.text)
    return render_template('index_ueberlieferung.html', title='Texte', files=files, url=request.url)


@app.route('/sammlung/<name>/text/<text>', methods=['GET'])
def sammlung_text(name, text):
    response = requests.get(beckend_endpoint + "/sammlung/{}/text/{}".format(name, text))
    files = json.loads(response.text)
    return_list = []
    for form in files:
        return_list.append([form[0], form[1]])
    return render_template('index_ueberlieferung_text.html', title='Text', files=return_list,
                           url=request.url, len=len(return_list), backups=get_backup_list(name, text))


@app.route('/sammlung/<name>/text/<text>/backups', methods=['GET'])
def backups_of_text(name, text):

    url = str(request.url).replace("/backups", "")
    return render_template('index_backups.html', title='Backups', backups=get_backup_list(name, text),
                           url=url)


@app.route('/sammlung/<name>/text/<text>/backup/<backup>', methods=['GET'])
def backup_of_text(name, text, backup):
    response = requests.get(beckend_endpoint + "/sammlung/{}/text/{}/backup/{}".format(name, text, backup))
    files = json.loads(response.text)
    return_list = []
    for form in files:
        return_list.append([form[0], form[1]])
    return render_template('index_backup_text.html', title='Backup', files=return_list,
                           url=request.url, len=len(return_list))


@app.route('/sammlung/<name>/text/<text>/backup/<backup>', methods=['POST'])
def restore_backup(name, text, backup):
    url = beckend_endpoint + "/sammlung/{}/text/{}/backup/{}".format(name, text, backup)
    requests.post(url)
    return redirect(url_for("sammlung_text", name=name, text=text))


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
    requests.post(url, json=json.dumps(erg, ensure_ascii=False))
    return redirect(url_for("sammlung_text", name=name, text=text))
