from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/about")
def harry():
    name = "happpy"
    return render_template("about.html",name2 = name)

@app.route("/bootstrap")
def bootstrap():
    name = "happpy"
    return render_template("bootstrap.html")

app.run(debug = True)