from flask import Flask, render_template, git, url_for, flash, redirect, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
# @app.route("/update_server", methods=["POST"])
# def update_server():
#     return "OK", 200
@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/jcham28/Project-2')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
