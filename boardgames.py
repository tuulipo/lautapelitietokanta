import db

def add_boardgame(boardgame_name, duration, players_min, players_max, age_limit, genre, user_id):
    sql = """INSERT INTO boardgames (boardgame_name, duration, players_min, players_max, age_limit, genre, user_id) 
             VALUES (?, ?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [boardgame_name, duration, players_min, players_max, age_limit, genre, user_id])