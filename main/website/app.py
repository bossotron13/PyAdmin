from flask import Flask, render_template, request, redirect, url_for
import logging, os, hashlib, random, string
import main.website.ApiShare as ApiShare

app = Flask(__name__)

Api = ApiShare.returnApi()

SessionIDS = []


def ReqStat():
    return Api.RequestStatus()

@app.route("/",  methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get("login"):
            username = hashlib.sha256(
                bytes(request.form.get("uname"), 'utf-8')).hexdigest()
            password = hashlib.sha256(
                bytes(request.form.get("psw"), 'utf-8')).hexdigest()
            
            if Api.ConfigDict["U256"] == username and Api.ConfigDict["P256"] == password:
                SID = ''.join(random.choices(
                    string.ascii_uppercase + string.ascii_lowercase + string.digits, k=32))
                SessionIDS.append(SID)
        else:
            SID = None
        return redirect('/', SessionID=SID)

    elif request.method == 'GET':
        return render_template("login.html", SessionID=None)

    #return render_template("button.html", status=ReqStat())


@app.route("/start")
def startServer():
    Api.SendCommand("start")
    return redirect('/')


@app.route("/restart")
def restartServer():
    Api.SendCommand("restart")
    return redirect('/')


@app.route("/stop")
def stopServer():
    Api.SendCommand("stop")
    return redirect('/')

app.run(port=5000, host="192.168.1.146", threaded=True)
