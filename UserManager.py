# UserManager


import MySQLdb


class UserManager:
    # def __init__(self):
    print("Hi")
    #     self.selected_player_id = None


    # def select_player(self, id):
    #     self.selected_player_id = id

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


def save_score(player_id, score):
    db = MySQLdb.connect(DB_HOST,
                         DB_USER,
                         DB_PASSWORD,
                         DB_NAME)
    cursor = db.cursor()
    cursor.execute('INSERT INTO scores (player_id, score) VALUES (%(player_id)s, %(score)s)',
                   {'player_id': player_id, 'score': score})
    db.commit()
    db.close()


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
    cursor.execute("""INSERT INTO scores (record_id, player_id, score) VALUES (201, 11, 200)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, score) VALUES (202, 11, 400)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, score) VALUES (203, 11, 300)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, score) VALUES (204, 11, 500)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, score) VALUES (205, 12, 122)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, score) VALUES (206, 12, 322)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, score) VALUES (207, 12, 222)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, score) VALUES (208, 13, 1201)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, score) VALUES (209, 13, 101)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, score) VALUES (210, 13, 1)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, score) VALUES (211, 13, 301)""")
    cursor.execute("""INSERT INTO scores (record_id, player_id, score) VALUES (212, 13, 11)""")

    db.commit()
    db.close()


    save_score(create_player("New Guy"), 1000000)
    print("Database seeded successfully!")


# --------------------------------
# Main Program
reset_database()
print(player_list())
print("-" * 40)
print(score_list())


# MySQL DataBase Setup
# ```sql
# use Handle;
# CREATE DATABASE Handle;
# CREATE USER 'user'@'localhost' IDENTIFIED BY 'user';
# GRANT ALL ON Handle.* TO user@localhost;
# ```
