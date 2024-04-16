from flask import Flask, render_template, redirect, session
import sqlite3 as sq

app = Flask(__name__)


@app.route("/")
def index():
    if session.new:
        return redirect("/login")
    else:
        return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.post("/login")
def verify_login():
    return True


if __name__ == "__main__":
    app.run(debug=True)