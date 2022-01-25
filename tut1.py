from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/harry")
def harry():
    return "<p>Hello, to Harry!</p>"

app.run(debug = True)