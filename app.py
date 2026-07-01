import git
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy

from forms import RegistrationForm

app = Flask(__name__)
proxied = FlaskBehindProxy(app)

# Secret key for WTForms
app.config["SECRET_KEY"] = "ee40137d434beb7618156749bc5ba660"

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# Create database tables
with app.app_context():
    db.create_all()

# Home route
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Save user to database
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()

        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))

    return render_template("register.html", title="Register", form=form)

# GitHub webhook auto-update route
@app.route("/update_server", methods=['POST'])
def update_server():
    repo = git.Repo('/home/jcham28/Project-2')
    origin = repo.remotes.origin
    origin.pull()
    return 'Updated PythonAnywhere successfully', 200

# Run locally
if __name__ == "__main__":
    app.run(debug=True)

