from flask import Flask, render_template, redirect, session, request, send_from_directory
import settings
import sqlite3 as sq
import hashlib
from datetime import datetime
import time
import os

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY

if not os.path.exists("images"):
    os.makedirs("images")



@app.before_request
def login_middleware():
    path = request.path
    protected_routes = ["/", "/add-nota", "/user", "/api/add-nota", "/api/user-info",
                        "/api/add-user", "/api/tipologie", "/api/users", "/users", "/api/roles"]
    dynamic_protected_routes = ["/api/user-notes", "/api/image", "/api/add-tipologia"]
    if (path in protected_routes or any([path.startswith(route) for route in dynamic_protected_routes])) and ("logged" not in session or not session["logged"]):
        session["logged"] = False
        session.modified = True
        return redirect("/login")

@app.before_request
def permissions():
    path = request.path
    protected_routes = ["/api/users", "/api/add-user", "/users", "/api/roles", "/api/add-tipologia"]
    if path in protected_routes and (session.get("role") != "admin"):
        return "Need admin role!", 403


def query(sql, data=None):
    if data is None:
        data = []
    con = sq.connect("data.db")
    cur = con.cursor()
    res = cur.execute(sql, data).fetchall()
    con.commit()
    con.close()
    return res


@app.route("/")
def index():
    page = request.args.get('page') if request.args.get('page') else 1
    max_page = query("SELECT COUNT(*) FROM Nota INNER JOIN Utente ON Nota.idUtente = Utente.id WHERE Utente.username = ?", [session["user"]])[0][0] // 10 + 1
    return render_template("index.html", page=int(page), max_page=max_page, is_admin=session["role"]=="admin")


@app.route("/login")
def login():
    if "logged" not in session or not session["logged"]:
        return render_template("login.html")
    else:
        return redirect("/")


@app.get("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/add-nota")
def add_nota_route():
    return render_template("aggiunta.html", is_admin=session["role"]=="admin")


@app.route("/user")
def user_route():
    user_info = get_user_info()
    return render_template("utente.html", is_admin=session["role"]=="admin", user_info=user_info)


@app.route("/add-user")
def add_user_route():
    return render_template("aggiunta_utente.html")


@app.route("/users")
def users_route():
    return render_template("dipendenti.html")


@app.route("/add-tipologia")
def add_tipologia_route():
    return render_template("aggiunta_tipologia.html")


@app.post("/api/add-nota")
def add_nota():
    image = request.files["image"]
    username = session["user"]
    timestamp = str(time.time())
    file_name = f"{username}_{timestamp}.{image.filename.split('.')[-1]}"
    image.save(f"images/{file_name}")
    data = [time.mktime(datetime.strptime(request.form["data"],
                                            "%Y-%m-%d").timetuple()), request.form["importo"], session["id"], request.form["tipologia"], file_name]
    query("INSERT INTO Nota (data, importo, idUtente, idTipologia, immagine) VALUES (?, ?, ?, ?, ?)", data)
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
                    [request.form["username"]])[0][0]
        session["id"] = res[0][0]
        session.modified = True
        return redirect("/")
    else:
        return redirect("/login")


@app.get("/api/user-notes/<page>")
def get_notes_of_user(page):
    username = session["user"]
    res = query("SELECT Nota.*, Tipologia.descrizione as descrizione FROM Nota "
                      "INNER JOIN Utente ON Utente.id = Nota.idUtente "
                      "INNER JOIN Tipologia ON Tipologia.id = Nota.idTipologia "
                      "WHERE username=? "
                      "LIMIT ?, ?", [username, (int(page) - 1) * 10 if page else 0, int(page) * 10 if page else 10])
    res = [{'data': datetime.fromtimestamp(row[1]).strftime("%d/%m/%Y"), 'importo': row[2], 'allegato': row[5], 'tipologia': row[6]} for row in res]
    return res


@app.get("/api/user-info")
def get_user_info():
    username = session["user"]
    data = query("SELECT * FROM Utente INNER JOIN Ruolo ON Utente.idRuolo = Ruolo.id WHERE Utente.username = ?", [username])[0]
    spese_totali = 0
    result = query("SELECT SUM(Nota.importo) FROM Nota INNER JOIN Utente ON Nota.idUtente = Utente.id WHERE Utente.username = ?", [username])
    if result[0][0] is not None:
        spese_totali = round(result[0][0], 2)
    #spese_totali = round(query("SELECT SUM(Nota.importo) FROM Nota INNER JOIN Utente ON Nota.idUtente = Utente.id WHERE Utente.username = ?", [username])[0][0], 2)
    numero_spese = query(
        "SELECT COUNT(*) FROM Nota INNER JOIN Utente ON Nota.idUtente = Utente.id WHERE Utente.username = ?",
        [username])[0][0]
    return {'nome': data[1], 'cognome': data[2], 'username': data[4], 'dataAssunzione': datetime.fromtimestamp(data[6] if data[6] else 0).strftime("%d/%m/%Y"), "speseTotali": spese_totali, "numeroSpese": numero_spese, "ruolo": data[8].title()}


@app.post("/api/add-user")
def add_user():
    if len(query("SELECT * FROM Utente WHERE username = ?", [request.form["username"]])) > 0:
        return redirect("/")
    password = request.form["password"]
    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    hash_password = hash_object.hexdigest()
    query("INSERT INTO Utente (nome, cognome, username, password, dataAssunzione, idRuolo) VALUES (?, ?, ?, ?, ?, 2)",
                [request.form["nome"], request.form["cognome"], request.form["username"], hash_password, time.mktime(datetime.strptime(request.form["data"],
                                            "%Y-%m-%d").timetuple())])
    return redirect("/")


@app.get("/api/tipologie")
def get_tipologie():
    tipologie = query("SELECT * FROM Tipologia")
    return [{"id": tipologia[0], "descrizione": tipologia[1]} for tipologia in tipologie]


@app.get("/api/users")
def get_all_users():
    res = query("SELECT * FROM Utente INNER JOIN Ruolo ON Utente.idRuolo = Ruolo.id")
    return [{"nome": row[1], "cognome": row[2], "username": row[4], "dataAssunzione": datetime.fromtimestamp(row[6]).strftime("%d/%m/%Y"), "ruolo": row[8]} for row in res]


@app.get("/api/roles")
def get_all_roles():
    res = query("SELECT * FROM Ruolo")
    return [{'id': row[0], 'nome': row[1]} for row in res]



@app.get("/api/image/<file_name>")
def get_image(file_name):
    splitted_file_name = file_name.split('_')
    if splitted_file_name[0] != session["user"]:
        return "Not your file!", 403
    if not os.path.exists(f"images/{file_name}"):
        return "File not found!", 404
    return send_from_directory("images", file_name)



@app.post("/api/add-tipologia")
def add_tipologia():
    query("INSERT INTO Tipologia (descrizione) VALUES (?)", [request.form["descrizione"]])
    return redirect("/")




if __name__ == "__main__":
    app.run(debug=True)
