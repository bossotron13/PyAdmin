from flask import Flask, render_template, request
from livereload import Server
import os


os.chdir(os.path.dirname(os.path.dirname(
    os.path.realpath(__file__))) + "/website")

app = Flask(__name__)

ButtonPressed = 0

@app.route("/")
def index():
    return render_template("button.html", ButtonPressed = ButtonPressed)

@app.route("/apple", methods=['GET', 'POST'])
def handle_form():
    global ButtonPressed
    ButtonPressed += 1
    return render_template("button.html", ButtonPressed=ButtonPressed)





if __name__ == "__main__":
    app.run(port=5000, debug=True)
