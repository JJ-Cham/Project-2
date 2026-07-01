from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/update_server", methods=["POST"])
def update_server():
    return "OK", 200

