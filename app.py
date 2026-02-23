from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "chatmate_secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

UPLOAD_FOLDER = "static/audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

messages = []

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@login_required
def home():
    return render_template("index.html", user=current_user.username)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/send", methods=["POST"])
@login_required
def send():
    data = request.json
    messages.append({
        "type": "text",
        "user": current_user.username,
        "message": data["message"]
    })
    return jsonify({"status": "ok"})

@app.route("/upload_audio", methods=["POST"])
@login_required
def upload_audio():
    audio = request.files["audio"]
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".webm"
    path = os.path.join(UPLOAD_FOLDER, filename)
    audio.save(path)

    messages.append({
        "type": "audio",
        "user": current_user.username,
        "file": filename
    })

    return jsonify({"status": "ok"})

@app.route("/messages")
@login_required
def get_messages():
    return jsonify(messages)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)