from flask import Flask, render_template, redirect, session, request
import settings
import sqlite3 as sq
import hashlib
from datetime import datetime

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
    con = sq.connect("data.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM Utente WHERE username=? AND password=?", [request.form["username"], hash_password]).fetchall()
    if len(res) > 0:
        session["logged"] = True
        session["user"] = request.form["username"]
        session["role"] = cur.execute("SELECT Ruolo.nome FROM Utente INNER JOIN Ruolo ON Ruolo.id = Utente.idRuolo WHERE username=?", [request.form["username"]]).fetchall()[0][0]
        session.modified = True
        con.close()
        return redirect("/")
    else:
        con.close()
        return redirect("/login")


@app.get("/api/user-notes")
def get_notes_of_user():
    if "logged" not in session or not session["logged"]:
        return redirect("/login")
    username = session["user"]
    con = sq.connect("data.db")
    cur = con.cursor()
    res = cur.execute("SELECT Nota.*, Tipologia.descrizione as descrizione FROM Nota "
                      "INNER JOIN Utente ON Utente.id = Nota.idUtente "
                      "INNER JOIN Tipologia ON Tipologia.id = Nota.idTipologia "
                      "WHERE username=?", [username]).fetchall()
    res = [{'data': datetime.fromtimestamp(row[1]).strftime("%m/%d/%Y"), 'importo': row[2], 'tipologia': row[5]} for row in res]
    return res


@app.get("/api/user-info")
def get_user_info():
    if "logged" not in session or not session["logged"]:
        return redirect("/login")
    username = session["user"]
    return username


@app.post("/api/add-user")
def add_user():
    if "logged" not in session or not session["logged"]:
        return redirect("/login")
    if session["role"] != "admin":
        return "Need admin role!", 403
    password = request.form["password"]
    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    hash_password = hash_object.hexdigest()
    con = sq.connect("data.db")
    cur = con.cursor()
    cur.execute("INSERT INTO Utente (nome, cognome, username, password, idRuolo) VALUES (?, ?, ?, ?, 2)",
                      [request.form["nome"], request.form["cognome"], request.form["username"], hash_password])
    con.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)