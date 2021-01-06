import json
from flask import render_template
from app import app
from flask import request
import requests
import configparser

config = configparser.ConfigParser()
config.read('E:\git\CorrectFrontend\.config')
beckend_endpoint = config['BACKEND']['ip'] + ":" + config['BACKEND']['port']



@app.route('/')
def ueberlieferung():
    if 'ueberlieferung' in request.args:
        ueberlieferung = request.args["ueberlieferung"]
        if 'text' in request.args:
            text = request.args["text"]
            response = requests.get(beckend_endpoint + "/files?ueberlieferung=" + ueberlieferung + "&text=" + text)
            files_temp = json.loads(response.text)
            files = []
            for file in files_temp:
                files.append([file, files_temp[file]])
            return render_template('index_ueberlieferung_text.html', title='Home', files=files, url=request.url)
        else:
            response = requests.get(beckend_endpoint + "/files?ueberlieferung=" + ueberlieferung)
            files = json.loads(response.text)
            return render_template('index_ueberlieferung.html', title='Home', files=files, url=request.url)
    else:
        response = requests.get(beckend_endpoint + "/files")
        files = json.loads(response.text)
        return render_template('index.html', title='Home', files=files, url=request.url)