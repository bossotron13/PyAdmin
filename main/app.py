from flask import Flask, render_template, request, redirect, url_for
import os, logging
from main import quitPy


app = Flask(__name__)

app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True

@app.route("/")
def index():
    return render_template("button.html")


@app.route("/stop")
def stopServer():
    quitPy()
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
