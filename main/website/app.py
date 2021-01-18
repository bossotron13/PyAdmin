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
    Api.StartServer()
    return redirect('/')


@app.route("/restart")
def restartServer():
    Api.RestartServer()
    return redirect('/')


@app.route("/stop")
def stopServer():
    Api.StopServer()
    return redirect('/')


'''
@app.route("/apple", methods=['GET', 'POST'])
def handle_form():
    global ButtonPressed
    ButtonPressed += 1
    print(request.args)
    return redirect('/')
'''

app.run(port=5000, host="192.168.1.146", threaded=True)
