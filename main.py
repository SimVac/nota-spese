from flask import Flask, render_template, redirect, session, request
import settings
import sqlite3 as sq
import hashlib
from datetime import datetime
import time

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY


def query(sql, data):
    con = sq.connect("data.db")
    cur = con.cursor()
    res = cur.execute(sql, data).fetchall()
    con.commit()
    con.close()
    return res


@app.route("/")
def index():
    if "logged" not in session or not session["logged"]:
        session["logged"] = False
        session.modified = True
        return redirect("/login")
    else:
        page = request.args.get('page') if request.args.get('page') else 1
        max_page = query("SELECT COUNT(*) FROM Nota INNER JOIN Utente ON Nota.idUtente = Utente.id WHERE Utente.username = ?", [session["user"]])[0][0] // 10 + 1
        return render_template("index.html", page=int(page), max_page=15)


@app.route("/login")
def login():
    if "logged" not in session or not session["logged"]:
        return render_template("login.html")
    else:
        return redirect("/")


@app.route("/add-nota")
def add_nota_route():
    if "logged" not in session or not session["logged"]:
        return redirect("/login")
    return render_template("aggiunta.html")


@app.route("/user")
def user_route():
    if "logged" not in session or not session["logged"]:
        return redirect("/login")
    return render_template("utente.html")


@app.post("/api/add-nota")
def add_nota():
    if "logged" not in session or not session["logged"]:
        return redirect("/login")
    data = [time.mktime(datetime.strptime(request.form["data"],
                                            "%Y-%m-%d").timetuple()), request.form["importo"], session["id"], 1]
    query("INSERT INTO Nota (data, importo, idUtente, idTipologia) VALUES (?, ?, ?, ?)", data)
    return redirect("/")


@app.post("/login")
def verify_login():
    password = request.form["password"]
    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    hash_password = hash_object.hexdigest()
    res = query("SELECT * FROM Utente WHERE username=? AND password=?", [request.form["username"], hash_password])
    if len(res) > 0:
        session["logged"] = True
        session["user"] = request.form["username"]
        session["role"] = query("SELECT Ruolo.nome FROM Utente INNER JOIN Ruolo ON Ruolo.id = Utente.idRuolo WHERE username=?",
                    [request.form["username"]])
        session["id"] = res[0][0]
        session.modified = True
        return redirect("/")
    else:
        return redirect("/login")


@app.get("/api/user-notes")
def get_notes_of_user():
    if "logged" not in session or not session["logged"]:
        return redirect("/login")
    username = session["user"]
    res = query("SELECT Nota.*, Utente.nome, Tipologia.descrizione as descrizione FROM Nota "
                      "INNER JOIN Utente ON Utente.id = Nota.idUtente "
                      "INNER JOIN Tipologia ON Tipologia.id = Nota.idTipologia "
                      "WHERE username=?", [username])
    res = [{'data': datetime.fromtimestamp(row[1]).strftime("%d/%m/%Y"), 'importo': row[2], 'nome': row[5], 'tipologia': row[6]} for row in res]
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
    query("INSERT INTO Utente (nome, cognome, username, password, idRuolo) VALUES (?, ?, ?, ?, 2)",
                [request.form["nome"], request.form["cognome"], request.form["username"], hash_password])
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
