from flask import Flask, render_template, redirect, session
import settings
import sqlite3 as sq

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY


@app.route("/")
def index():
    if "logged" not in session or not session["logged"]:
        session["logged"] = False
        session.modified = True
        return redirect("/login")
    else:
        return render_template("index.html")


@app.route("/login")
def login():
    if session["logged"]:
        return redirect("/")
    else:
        return render_template("login.html")


@app.post("/login")
def verify_login():
    session["logged"] = True
    session.modified = True
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)