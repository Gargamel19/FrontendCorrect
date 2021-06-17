import json
from datetime import datetime

from flask import render_template, redirect, url_for, request, flash
from werkzeug.urls import url_parse

from app import app
import requests

import smtplib

from app.forms import LoginForm, RegistrationForm, PWCForm, RequestOTLForm, MAILCForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required


my_ip = app.config["MY_IP"]
backend_endpoint = app.config["BACKEND_IP"]
port = app.config["BACKEND_PORT"]
if port != 80:
    backend_endpoint = backend_endpoint + ":" + str(port)
print(backend_endpoint)

# # # # # # MAILS # # # # # #

mail_user = app.config["MAIL_USERNAME"]
mail_password = app.config["MAIL_SECRET"]
smtp_server = app.config["SMTP_SERVER"]
TLS_PORT = app.config["TLS_PORT"]

# # # # # # Mails end # # # # # #

selected = ""


def add_user(username, email, password, super_user):
    user = User(username=username, email=email, super_user=super_user)
    exists = User.query.filter_by(username=username).first()
    if not exists:
        user.set_password(password)
        user.save_user()

def send_mail(receiver, subject, text):
    mail_text = text
    data = 'From:' + mail_user + "\nTo:" + receiver + "\nSubject:" + subject + "\n\n" + mail_text
    server = smtplib.SMTP(smtp_server + ":" + TLS_PORT)
    server.starttls()
    server.login(mail_user, mail_password)
    server.sendmail(mail_user, receiver, data)
    server.quit()


def get_backup_list(name, text):
    response = requests.get(backend_endpoint + "/sammlung/{}/text/{}/backups".format(name, text))
    backups = json.loads(response.text)
    new_backups = []
    for backup in backups:
        content = backup.replace("_r_.xml", "").split("-")[1:]
        print(int(content[0]), int(content[1]), int(content[2]), int(content[3]), int(content[4]),
              int(content[5].split(".")[0]))
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
        user_dummy = User.query.filter_by(username=form.username.data).first()
        if user_dummy is None or not user_dummy.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user_dummy, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('ueberlieferung')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('ueberlieferung'))


def get_username_from_current_user(current_user):
    return User.query.filter_by(id=current_user.get_id()).first().username


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    username = get_username_from_current_user(current_user)
    if current_user.is_authenticated:
        logged_in_user = User.query.filter_by(id=current_user.get_id()).first()
        if logged_in_user.super_user:
            form = RegistrationForm()
            if form.validate_on_submit():
                user_dummy = User(username=form.username.data, email=form.email.data, super_user=False)
                user_dummy.set_password(form.password.data)
                user_dummy.save_user()
                send_mail(user_dummy.email, "anmeldung war erfolgreich",
                          "your registration was successfull: " + my_ip + "/login")
                return 'Congratulations, you are now a registered user!'
            return render_template('register.html', title='Register', form=form, username=username)
    return "YOU ARE NOT ALLOWED TO CREATE A NEW USER"


@app.route('/change_pw', methods=['GET', 'POST'])
def change_pw():
    if "otl" in request.args:
        otl = request.args["otl"]
        user_dummy = User.query.filter_by(one_time_link_hash=otl).first()
        form = PWCForm()
        if form.validate_on_submit():
            if user_dummy.one_time_link_date > datetime.now():
                user_dummy.set_password(form.password.data)
                user_dummy.save_user()
                return 'Congratulations, you have changed your PW'
            return "The Link has been aspired"
        return render_template('change_pw.html', title='Change_PW', form=form)
    else:
        if current_user.is_authenticated:
            username = get_username_from_current_user(current_user)
            form = PWCForm()
            if form.validate_on_submit():
                user_dummy = User.query.filter_by(id=current_user.get_id()).first()
                user_dummy.set_password(form.password.data)
                user_dummy.save_user()
                return redirect(url_for('login'))
            return render_template('change_pw.html', title='Change_PW', form=form, username=username)
        else:
            form = RequestOTLForm()
            if form.validate_on_submit():
                if User.query.filter_by(username=form.username.data).first():
                    user_dummy = User.query.filter_by(username=form.username.data).first()
                    otl = user_dummy.make_one_time_link()
                    url = my_ip + "/change_pw?otl=" + otl
                    send_mail(user_dummy.email, "Verifizierung der aenderung ihres Passwords",
                              "Click this link to change your Password: " + url)
                    return "CHECK YOUT E-MAIL"
                else:
                    return "USER HAS NOT BEEN FOUND"
            return render_template('request_otl.html', title='Change_Password', form=form)


@app.route('/change_mail', methods=['GET', 'POST'])
def change_mail():
    if "otl" in request.args:
        if "email" in request.args:
            otl = request.args["otl"]
            email = request.args["email"]
            user_dummy = User.query.filter_by(one_time_link_hash=otl).first()
            user_dummy.set_mail(email)
            user_dummy.save_user()
            return redirect(url_for('login'))
    if current_user.is_authenticated:
        username = get_username_from_current_user(current_user)
        form = MAILCForm()
        user_dummy = User.query.filter_by(id=current_user.get_id()).first()
        if form.validate_on_submit():
            otl = user_dummy.make_one_time_link()
            url = my_ip + "/change_mail?otl=" + otl + "&email=" + form.mail1.data
            send_mail(user_dummy.email, "Verifizierung der Änderung ihrer E-Mail-Adresse",
                      "Click this link to change your email to: " + url)
        return render_template('change_mail.html', title='Change_MAIL', form=form, username=username)
    else:
        return redirect(url_for('login'))


@app.route('/', methods=['GET'])
@login_required
def ueberlieferung():
    username = get_username_from_current_user(current_user)
    response = requests.get(backend_endpoint + "/sammlungen")
    print(backend_endpoint + "/sammlungen")
    print(response.text)
    files = json.loads(response.text)
    return render_template('index.html', title='Home', files=files, url=request.url, username=username)


@app.route('/sammlung/<name>', methods=['GET'])
@login_required
def sammlung(name):
    username = get_username_from_current_user(current_user)
    response = requests.get(backend_endpoint + "/sammlung/" + name)
    files = json.loads(response.text)
    return render_template('index_ueberlieferung.html', title='Texte', files=files, url=request.url, username=username)


@app.route('/sammlung/<name>/text/<text>', methods=['GET'])
@login_required
def sammlung_text(name, text):
    username = get_username_from_current_user(current_user)
    response = requests.get(backend_endpoint + "/sammlung/{}/text/{}".format(name, text))
    files = json.loads(response.text)
    return_list = []
    for form in files:
        return_list.append([form[0], form[1]])
    return render_template('index_ueberlieferung_text.html', title='Text', files=return_list,
                           url=request.url, len=len(return_list), backups=get_backup_list(name, text), username=username)


@app.route('/sammlung/<name>/text/<text>/backups', methods=['GET'])
@login_required
def backups_of_text(name, text):
    username = get_username_from_current_user(current_user)
    url = str(request.url).replace("/backups", "")
    return render_template('index_backups.html', title='Backups', backups=get_backup_list(name, text),
                           url=url, username=username)


@app.route('/sammlung/<name>/text/<text>/backup/<backup>', methods=['GET'])
@login_required
def backup_of_text(name, text, backup):
    username = get_username_from_current_user(current_user)
    response = requests.get(backend_endpoint + "/sammlung/{}/text/{}/backup/{}".format(name, text, backup))
    files = json.loads(response.text)
    return_list = []
    for form in files:
        return_list.append([form[0], form[1]])
    return render_template('index_backup_text.html', title='Backup', files=return_list,
                           url=request.url, len=len(return_list), username=username)


@app.route('/sammlung/<name>/text/<text>/backup/<backup>', methods=['POST'])
@login_required
def restore_backup(name, text, backup):
    username = get_username_from_current_user(current_user)
    url = backend_endpoint + "/sammlung/{}/text/{}/backup/{}".format(name, text, backup)
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
            erg[len(erg) - 1][0].append(request.form.get(key))
    url = backend_endpoint + "/sammlung/{}/text/{}".format(name, text)
    requests.post(url, json=json.dumps(erg, ensure_ascii=False))
    return redirect(url_for("sammlung_text", name=name, text=text))
