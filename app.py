import sqlite3
import secrets

from flask import Flask
from flask import abort, flash, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash

import config
import db
import boardgames

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)

    if request.form["csrf_token"] != session.get("csrf_token"):
        abort(403)

@app.route("/")
def index():
    all_boardgames = boardgames.get_boardgames()
    return render_template("index.html", boardgames = all_boardgames)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")

    if not username or len(username) > 50:
        flash("VIRHE: virheellinen käyttäjätunnus")
        return redirect("/register")

    if not password1:
        flash("VIRHE: salasana ei voi olla tyhjä")
        return redirect("/register")

    password_hash = generate_password_hash(password1)

    try:
        sql = """INSERT INTO users (username, password_hash)
                 VALUES (?, ?)"""

        db.execute(sql, [username, password_hash])

    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    flash("Tunnus luotu. Voit nyt kirjautua sisään.")
    return redirect("/login")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    sql = """SELECT id, password_hash
             FROM users
             WHERE username = ?"""

    rows = db.query(sql, [username])

    if not rows:
        flash("VIRHE: väärä tunnus tai salasana")
        return redirect("/login")

    result = rows[0]
    user_id = result["id"]
    password_hash = result["password_hash"]

    if check_password_hash(password_hash, password):
        session.clear()
        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)

        return redirect("/")

    flash("VIRHE: väärä tunnus tai salasana")
    return redirect("/login")

@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")

@app.route("/new_boardgame")
def new_boardgame():
    require_login()
    return render_template("new_boardgame.html")

@app.route("/create_boardgame", methods=["POST"])
def create_boardgame():
    require_login()
    check_csrf()

    boardgame_name = request.form["boardgame_name"]
    duration = request.form["duration"]
    players_min = request.form["players_min"]
    players_max = request.form["players_max"]
    age_limit = request.form["age_limit"]
    genre = request.form["genre"]
    user_id = session["user_id"]

    if not boardgame_name or len(boardgame_name) > 100:
        abort(403)

    user_id = session["user_id"]

    boardgame_id = boardgames.add_boardgame(
        boardgame_name,
        duration,
        players_min,
        players_max,
        age_limit,
        genre,
        user_id)

    return redirect("/boardgame/" + str(boardgame_id))

@app.route("/find_boardgame")
def find_boardgame():
    query = request.args.get("query")

    if query:
        results = boardgames.find_boardgames(query)
    else:
        query = ""
        results = []

    return render_template(
        "find_boardgame.html",
        query=query,
        results=results
    )

@app.route("/edit_boardgame/<int:boardgame_id>")
def edit_boardgame(boardgame_id):
    require_login()

    boardgame = boardgames.get_boardgame(boardgame_id)

    if not boardgame:
        abort(404)

    if boardgame["user_id"] != session["user_id"]:
        abort(403)

    return render_template(
        "edit_boardgame.html",
        boardgame=boardgame
    )

@app.route("/update_boardgame", methods=["POST"])
def update_boardgame():
    require_login()
    check_csrf()

    boardgame_id = request.form["boardgame_id"]
    boardgame = boardgames.get_boardgame(boardgame_id)

    if not boardgame:
        abort(404)

    if boardgame["user_id"] != session["user_id"]:
        abort(403)

    boardgame_name = request.form["boardgame_name"]
    duration = request.form["duration"]
    players_min = request.form["players_min"]
    players_max = request.form["players_max"]
    age_limit = request.form["age_limit"]
    genre = request.form["genre"]

    if not boardgame_name or len(boardgame_name) > 100:
        abort(403)

    boardgames.update_boardgame(
        boardgame_id,
        boardgame_name,
        duration,
        players_min,
        players_max,
        age_limit,
        genre
    )

    return redirect("/boardgame/" + str(boardgame_id))

@app.route("/remove_boardgame/<int:boardgame_id>",
           methods=["GET", "POST"])
def remove_boardgame(boardgame_id):
    require_login()

    boardgame = boardgames.get_boardgame(boardgame_id)

    if not boardgame:
        abort(404)

    if boardgame["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template(
            "remove_boardgame.html",
            boardgame=boardgame
        )

    if request.method == "POST":
        check_csrf()

        if "remove" in request.form:
            boardgames.remove_boardgame(boardgame_id)
            return redirect("/")

        return redirect("/boardgame/" + str(boardgame_id))

@app.route("/boardgame/<int:boardgame_id>")
def show_boardgame(boardgame_id):
    boardgame = boardgames.get_boardgame(boardgame_id)
    if not boardgame:
        abort(404)

    return render_template("show_boardgame.html", boardgame=boardgame)