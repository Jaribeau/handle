# UserManager


import MySQLdb

DB_HOST = "localhost"
DB_USER = "user"
DB_PASSWORD = "user"
DB_NAME = "Handle"


def player_list():
    db = MySQLdb.connect(DB_HOST,
                         DB_USER,
                         DB_PASSWORD,
                         DB_NAME)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM players')
    players = cursor.fetchall()

    # for player in cursor.fetchall():
    #     print(player)
    #     players.append(player[0])

    db.commit()
    db.close()
    return players


def score_list():
    db = MySQLdb.connect(DB_HOST,
                         DB_USER,
                         DB_PASSWORD,
                         DB_NAME)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM scores')
    scores = cursor.fetchall()

    # for player in cursor.fetchall():
    #     print(player)
    #     players.append(player[0])

    db.commit()
    db.close()
    return scores


def highscores():
    db = MySQLdb.connect(DB_HOST,
                         DB_USER,
                         DB_PASSWORD,
                         DB_NAME)
    cursor = db.cursor()
    cursor.execute('SELECT * FROM scores ORDER BY score DESC LIMIT 10')
    highscores_raw = cursor.fetchall()
    highscores = []

    for highscore in highscores_raw:
        highscores.append([highscore[2], highscore[3]])

    return highscores


def save_score(player_id, player_name, score):

    if type(player_id) is not int \
            or type(player_name) is not str \
            or type(score) is not int:
        return False

    try:
        db = MySQLdb.connect(DB_HOST,
                             DB_USER,
                             DB_PASSWORD,
                             DB_NAME)
        cursor = db.cursor()
        cursor.execute('INSERT INTO scores (player_id, player_name, score) VALUES (%(player_id)s, %(player_name)s, %(score)s)',
                       {'player_id': player_id, 'player_name': player_name, 'score': score})
        db.commit()

    except MySQLdb.IntegrityError:
        print("Failed to insert values: ", player_id, ", ", player_name, ", ", score)
        return False

    finally:
        db.close()

    return True


def create_player(player_name):
    db = MySQLdb.connect(DB_HOST,
                         DB_USER,
                         DB_PASSWORD,
                         DB_NAME)
    cursor = db.cursor()
    cursor.execute('INSERT INTO players (player_name) VALUES (%(player_name)s)',
                   {'player_name': player_name})
    new_player_id = db.insert_id()
    db.commit()
    db.close()
    return new_player_id


def table_exists(db, table_name):
    cursor = db.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(table_name.replace('\'', '\'\'')))
    if cursor.fetchone()[0] == 1:
        cursor.close()
        return True

    cursor.close()
    return False


def drop_tables():
    db = MySQLdb.connect(DB_HOST,
                         DB_USER,
                         DB_PASSWORD,
                         DB_NAME)
    cursor = db.cursor()
    cursor.execute("""SET foreign_key_checks = 0""")
    cursor.execute("""DROP TABLE if exists players""")
    cursor.execute("""DROP TABLE if exists scores""")
    cursor.execute("""SET foreign_key_checks = 1""")
    db.commit()
    db.close()


def setup_tables():
    db = MySQLdb.connect(DB_HOST,
                         DB_USER,
                         DB_PASSWORD,
                         DB_NAME)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Create tables

    if not table_exists(db, "players"):
        sql = """CREATE TABLE players (
            player_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            player_name CHAR(30))"""
        cursor.execute(sql)

    # Belongs to player
    if not table_exists(db, "scores"):
        sql = """CREATE TABLE scores (
            record_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            player_id INT NOT NULL,
            player_name CHAR(30),
            score INT NOT NULL,
            FOREIGN KEY fk_player(player_id)
            REFERENCES players(player_id)
            ON DELETE CASCADE)"""
        cursor.execute(sql)

    db.commit()

    # disconnect from server
    db.close()


def reset_database():
        drop_tables()
        setup_tables()
        seed()


def seed():
    db = MySQLdb.connect(DB_HOST,
                         DB_USER,
                         DB_PASSWORD,
                         DB_NAME)
    cursor = db.cursor()

    # -- PLAYER DATA --
    cursor.execute("""INSERT INTO players (player_id, player_name) VALUES (11, 'Jared')""")
    cursor.execute("""INSERT INTO players (player_id, player_name) VALUES (12, 'River')""")
    cursor.execute("""INSERT INTO players (player_id, player_name) VALUES (13, 'Igor')""")
    cursor.execute("""INSERT INTO players (player_id, player_name) VALUES (14, 'Jack')""")

    # -- SCORE DATA --
    cursor.execute("""INSERT INTO scores (record_id, player_id, player_name, score) VALUES (201, 11, 'Jared', 200)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, player_name, score) VALUES (202, 11, 'Jared', 400)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, player_name, score) VALUES (203, 11, 'Jared', 300)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, player_name, score) VALUES (204, 11, 'Jared', 500)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, player_name, score) VALUES (205, 12, 'River', 122)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, player_name, score) VALUES (206, 12, 'River', 322)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, player_name, score) VALUES (207, 12, 'River', 222)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, player_name, score) VALUES (208, 13, 'Igor', 1201)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, player_name, score) VALUES (209, 13, 'Igor', 101)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, player_name, score) VALUES (210, 13, 'Igor', 1)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, player_name, score) VALUES (211, 13, 'Igor', 301)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, player_name, score) VALUES (212, 13, 'Igor', 110000)""")

    db.commit()
    db.close()


    # save_score(create_player("New Guy"), 1000000)
    print("Database seeded successfully!")


# --------------------------------
# Main Program
# reset_database()
# print(player_list())
# print("-" * 40)
# print(score_list())


# MySQL DataBase Setup
# ```sql
# use Handle;
# CREATE DATABASE Handle;
# CREATE USER 'user'@'localhost' IDENTIFIED BY 'user';
# GRANT ALL ON Handle.* TO user@localhost;
# ```
