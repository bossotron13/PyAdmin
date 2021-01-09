from flask import Flask, render_template, request, redirect, url_for
import os, logging
import main.website.ApiShare as test

app = Flask(__name__)

Api =  test.returnApi()

app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True

@app.route("/")
def index():
    return render_template("button.html")


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

app.run(port=5000)
