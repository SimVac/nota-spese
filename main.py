from flask import Flask, render_template, redirect, session, request
import settings
import sqlite3 as sq
import hashlib

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
    if "logged" not in session or not session["logged"]:
        return render_template("login.html")
    else:
        return redirect("/")


@app.post("/login")
def verify_login():
    password = request.form["password"]
    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    hash_password = hash_object.hexdigest()
    data = [request.form["username"], hash_password]
    con = sq.connect("data.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM Utente WHERE username=? AND password=?", data)
    if len(res.fetchall()) > 0:
        session["logged"] = True
        session.modified = True
        return redirect("/")
    else:
        return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)