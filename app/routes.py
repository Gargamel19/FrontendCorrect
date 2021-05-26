import json
import os
import sqlite3
from datetime import datetime

from flask import render_template, redirect, url_for, request, flash
from werkzeug.urls import url_parse

from app import app
from app import db
import requests
import configparser

import smtplib

from app.forms import LoginForm, RegistrationForm, PWCForm, RequestOTLForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required

config = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
path_config = os.path.join(dir_path, ".config")
config.read(path_config)
port = config['BACKEND']['port']
beckend_endpoint = config['BACKEND']['ip']
if port != "80":
    beckend_endpoint = beckend_endpoint + ":" + port

server_adress = "http://localhost:5000"
##### MAILS ######
user = config["MAIL"]['user']
password = config["MAIL"]["user_secret"]
smtp_server = config["MAIL"]["smtp_server"]
TLS_PORT = config["MAIL"]["TLS_PORT"]
#### mails end #####
selected = ""


def send_mail(receiver, verify_hash):
    url = server_adress + "/change_pw?otl=" + verify_hash
    mail_text = "Click this link to change password " + url
    subject = "Verifizieren-FettarmQP"
    mail_from = user
    data = 'From:' + mail_from + "\nTo:" + receiver + "\nSubject:" + subject + "\n\n" + mail_text
    server = smtplib.SMTP(smtp_server + ":" + TLS_PORT)
    server.starttls()
    server.login(user, password)
    server.sendmail(mail_from, receiver, data)
    server.quit()


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('ueberlieferung'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('ueberlieferung')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('ueberlieferung'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('ueberlieferung'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/change_pw', methods=['GET', 'POST'])
def change_pw():
    if "otl" in request.args:
        otl = request.args["otl"]
        user = User.query.filter_by(one_time_link_hash=otl).first()
        form = PWCForm()
        if form.validate_on_submit():
            if user.one_time_link_date > datetime.now():
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Congratulations, you have changed your PW')
            flash('The Link has been aspired')
            return redirect(url_for('ueberlieferung'))
        return render_template('change_pw.html', title='Change_PW', form=form)
    else:
        if current_user.is_authenticated:
            form = PWCForm()
            if form.validate_on_submit():
                user = User.query.filter_by(id=current_user.get_id()).first()
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Congratulations, you have changed your PW')
                return redirect(url_for('ueberlieferung'))
            return render_template('change_pw.html', title='Change_PW', form=form)
        else:
            form = RequestOTLForm()
            if form.validate_on_submit():
                user = User.query.filter_by(username=form.username.data).first()
                otl = user.make_one_time_link()
                send_mail(user.email, otl)
            return render_template('request_otl.html', title='Change_Password', form=form)


@app.route('/', methods=['GET'])
@login_required
def ueberlieferung():
    response = requests.get(beckend_endpoint + "/sammlungen")
    files = json.loads(response.text)
    return render_template('index.html', title='Home', files=files, url=request.url)


@app.route('/sammlung/<name>', methods=['GET'])
@login_required
def sammlung(name):
    response = requests.get(beckend_endpoint + "/sammlung/" + name)
    files = json.loads(response.text)
    return render_template('index_ueberlieferung.html', title='Texte', files=files, url=request.url)


@app.route('/sammlung/<name>/text/<text>', methods=['GET'])
@login_required
def sammlung_text(name, text):
    response = requests.get(beckend_endpoint + "/sammlung/{}/text/{}".format(name, text))
    files = json.loads(response.text)
    return_list = []
    for form in files:
        return_list.append([form[0], form[1]])
    return render_template('index_ueberlieferung_text.html', title='Text', files=return_list,
                           url=request.url, len=len(return_list), backups=get_backup_list(name, text))


@app.route('/sammlung/<name>/text/<text>/backups', methods=['GET'])
@login_required
def backups_of_text(name, text):

    url = str(request.url).replace("/backups", "")
    return render_template('index_backups.html', title='Backups', backups=get_backup_list(name, text),
                           url=url)


@app.route('/sammlung/<name>/text/<text>/backup/<backup>', methods=['GET'])
@login_required
def backup_of_text(name, text, backup):
    response = requests.get(beckend_endpoint + "/sammlung/{}/text/{}/backup/{}".format(name, text, backup))
    files = json.loads(response.text)
    return_list = []
    for form in files:
        return_list.append([form[0], form[1]])
    return render_template('index_backup_text.html', title='Backup', files=return_list,
                           url=request.url, len=len(return_list))


@app.route('/sammlung/<name>/text/<text>/backup/<backup>', methods=['POST'])
@login_required
def restore_backup(name, text, backup):
    url = beckend_endpoint + "/sammlung/{}/text/{}/backup/{}".format(name, text, backup)
    requests.post(url)
    return redirect(url_for("sammlung_text", name=name, text=text))


@app.route('/sammlung/<name>/text/<text>', methods=['POST'])
@login_required
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
