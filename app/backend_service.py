import requests

from app import app

def get_sammlungen():
    response = requests.get(app.config["BACKEND_IP"] + "/sammlungen")
