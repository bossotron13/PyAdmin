from flask import Flask, render_template, request, redirect, url_for
import os
import logging
import main.website.ApiShare as ApiShare

app = Flask(__name__)

Api = ApiShare.returnApi()


def ReqStat():
    return Api.RequestStatus()


@app.route("/")
def index():
    return render_template("button.html", status=ReqStat())


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
