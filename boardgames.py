import db

def add_boardgame(boardgame_name, duration, players_min, players_max, age_limit, genre, user_id):
    sql = """INSERT INTO boardgames (boardgame_name, duration, players_min, players_max, age_limit, genre, user_id) 
             VALUES (?, ?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [boardgame_name, duration, players_min, players_max, age_limit, genre, user_id])

def get_boardgames():
    sql = "SELECT id, boardgame_name FROM boardgames ORDER BY boardgame_name"
    return db.query(sql)

def get_boardgame(boardgame_id):
    sql = """SELECT boardgames.id,
                    boardgames.boardgame_name,
                    boardgames.duration,
                    boardgames.players_min,
                    boardgames.players_max,
                    boardgames.age_limit,
                    boardgames.genre,
                    boardgames.user_id,
                    users.username
             FROM boardgames, users
             WHERE boardgames.user_id = users.id
             AND boardgames.id = ?"""

    result = db.query(sql, [boardgame_id])

    if not result:
        return None

    return result[0]


def add_boardgame(boardgame_name, duration, players_min,
                  players_max, age_limit, genre, user_id):

    sql = """INSERT INTO boardgames
             (boardgame_name, duration, players_min,
              players_max, age_limit, genre, user_id)
             VALUES (?, ?, ?, ?, ?, ?, ?)"""

    db.execute(sql, [boardgame_name, duration, players_min,
                     players_max, age_limit, genre, user_id])

    return db.last_insert_id()



def find_boardgames(query):
    sql = """SELECT id, boardgame_name
             FROM boardgames
             WHERE boardgame_name LIKE ?
                OR genre LIKE ?
             ORDER BY boardgame_name"""

    search = "%" + query + "%"

    return db.query(sql, [search, search])

def remove_boardgame(boardgame_id):
    sql = """DELETE FROM boardgames
             WHERE id = ?"""

    db.execute(sql, [boardgame_id])

def update_boardgame(boardgame_id, boardgame_name, duration,
                     players_min, players_max, age_limit, genre):

    sql = """UPDATE boardgames
             SET boardgame_name = ?,
                 duration = ?,
                 players_min = ?,
                 players_max = ?,
                 age_limit = ?,
                 genre = ?
             WHERE id = ?"""

    db.execute(sql, [boardgame_name, duration, players_min,
                     players_max, age_limit, genre, boardgame_id])