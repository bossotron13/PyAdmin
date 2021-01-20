from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from flask import Flask, render_template, request, redirect, url_for, make_response
import logging
import os
import hashlib
import random
import string
import sys
import time
import threading
import main.website.ApiShare as ApiShare


app = Flask(__name__)

Api = ApiShare.returnApi()

SessionIDS = []


def DumpedSessions():
    while True:
        time.sleep(60)
        if SessionIDS:
            if SessionIDS[1] != 0:
                SessionIDS[1] -= 1
            else:
                SessionIDS.clear()


def UpdateTime():
    if request.cookies.get('SessionID') in SessionIDS:
        SessionIDS[1] = 5


threading.Thread(target=DumpedSessions).start()

def ReqStat():
    return Api.RequestStatus()

@app.route("/",  methods=['GET', 'POST'])
def index():
    UpdateTime()
    if request.method == 'POST':
        if request.form.get("login"):
            if not request.cookies.get('SessionID') in SessionIDS:
                username = hashlib.sha256(
                    bytes(request.form.get("uname"), 'utf-8')).hexdigest()
                password = hashlib.sha256(
                    bytes(request.form.get("psw"), 'utf-8')).hexdigest()
                
                if Api.ConfigDict["U256"] == username and Api.ConfigDict["P256"] == password:
                    SID = ''.join(random.choices(
                        string.ascii_uppercase + string.ascii_lowercase + string.digits, k=32))
                    SessionIDS.clear()
                    SessionIDS.append(SID)
                    SessionIDS.append(5)
                    resp = make_response(render_template("login.html"))
                    resp.set_cookie('SessionID', SID)
                    return resp
            else:
                return render_template("login.html")
    elif request.method == 'GET':
        if request.cookies.get('SessionID') in SessionIDS:
            return redirect("/panel?SID=%s" % SessionIDS[0])
        else:
            return render_template("login.html")

    #return render_template("button.html", status=ReqStat())


@app.route("/start")
def startServer():
    UpdateTime()
    arg = request.args.get('SID', default="Null", type=str)
    if not arg in SessionIDS:
        return redirect('/')
    Api.SendCommand("start")
    return redirect('/')


@app.route("/cookie")
def cookie():
    UpdateTime()
    name = request.cookies.get('SessionID')
    return '<h1>welcome ' + name + '</h1>'


@app.route("/panel")
def panel():
    UpdateTime()
    arg = request.args.get('SID', default="Null", type=str)
    if not arg in SessionIDS:
        return redirect('/')
    return render_template("button.html")

@app.route("/restart")
def restartServer():
    UpdateTime()
    arg = request.args.get('SID', default="Null", type=str)
    if not arg in SessionIDS:
        return redirect('/')
    Api.SendCommand("restart")
    return redirect('/')


@app.route("/stop")
def stopServer():
    UpdateTime()
    arg = request.args.get('SID', default="Null", type=str)
    if not arg in SessionIDS:
        return redirect('/')
    Api.SendCommand("stop") 
    return redirect('/')


def CacheServer():
    class ClearCache(QWebEngineView):
        def Cache(self):
            self.view = QWebEngineView()
            self.view.page().profile().clearHttpCache()
            self.load(QUrl('http://127.0.0.1:5000'))

    app = QApplication(sys.argv)
    s = ClearCache()
    s.app = app
    s.Cache()
    sys.exit(app.exec_())



threading.Thread(target=CacheServer).start()
app.run(port=5000, host="127.0.0.1", threaded=True)
