import sqlite3

from GameStatus import GameStatus


# Grupo:
# RAQUEL FREIRE CERZOSIMO - 2020.1905.009-6
# RAISSA RINALDI YOSHIOKA - 2020.1905.049-5
# VITOR YUSKE WATANABE - 2020.1905.058-4


class DataBase:
    """
        Class responsible for all database interactions
        """
    def __init__(self, db_path=None):
        self.db_path = db_path or "storage.db"

        self.__check_connection()

    def __check_connection(self):
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            cur.execute(
                """SELECT * FROM users LIMIT 1""").fetchall()
        except sqlite3.OperationalError as error:
            print("[DATABASE] ERROR: Error reading data from table users, trying to create it\n", error)
            self.__create_table_users(cur)
        except sqlite3.Error as error:
            print("[DATABASE] ERROR: Error reading data from table\n", error)

        try:
            cur.execute(
                """SELECT * FROM games LIMIT 1""").fetchall()
        except sqlite3.OperationalError as error:
            print("[DATABASE] ERROR: Error reading data from table game, trying to create it\n", error)
            self.__create_table_games(cur)
        except sqlite3.Error as error:
            print("[DATABASE] ERROR: Error reading data from table\n", error)
        finally:
            if con:
                con.commit()
                con.close()

    def __create_table_users(self, cur):
        cur.execute('''
           CREATE TABLE users(
               username text,
               nick text,
               password text,
               status text,
               ip text,
               port text
               )''')
        print("[DATABASE] Table users created successfully")

    def __create_table_games(self, cur):
        cur.execute('''
           CREATE TABLE games(
                host_nick text,
                players text,
                status text,
                winner text NULLABLE
               )''')
        print("[DATABASE] Table games created successfully")

    def fetch_data(self, nick):
        user = None
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            sql_select_query = """SELECT * FROM users WHERE nick = ?"""
            cur.execute(sql_select_query, (nick,))

            user = cur.fetchone()

            if user is None:
                print("[DATABASE] INFO: Queried user (%s) not found" % nick)

        except sqlite3.Error as error:
            print("[DATABASE] ERROR: Error reading data from table\n", error)
        finally:
            if con:
                con.commit()
                con.close()

        return user

    def save_data(self, nick, username, password, status, ip, port):
        success = False
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            user = self.fetch_data(nick)
            if user:
                print("[DATABASE] User %s already exists, skipping creation" % nick)
                return False
            insert = """INSERT INTO users
                         (username ,nick, password, status, ip, port) 
                         VALUES (?, ?, ?, ?, ?, ?);"""

            data_tuple = (username, nick, password, status, ip, port)
            cur.execute(insert, data_tuple)
            print("[DATABASE] User %s data saved successfully" % nick)
            success = True
        except sqlite3.Error as error:
            print("[DATABASE] ERROR: Error saving data from table users\n", error)
        finally:
            if con:
                con.commit()
                con.close()
        return success

    def update_status(self, nick, status):
        success = False
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            insert = """UPDATE users SET
                         status = ?  WHERE nick = ?;"""

            data_tuple = (status, nick)
            cur.execute(insert, data_tuple)
            print("[DATABASE] User %s data saved successfully" % nick)
            success = True
        except sqlite3.Error as error:
            print("[DATABASE] ERROR: Error saving data from table users\n", error)
        finally:
            if con:
                con.commit()
                con.close()

        return success

    def update_connection(self, nick, status, ip, port):
        success = False
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            insert = """UPDATE users SET
                                status = ?, ip = ?, port = ? WHERE nick = ?"""

            data_tuple = (status, ip, port, nick)
            cur.execute(insert, data_tuple)
            print("[DATABASE] User %s data updated successfully" % nick)
            success = True
        except sqlite3.Error as error:
            print("[DATABASE] ERROR: Error updating data from table users\n", error)
        finally:
            if con:
                con.commit()
                con.close()

        return success

    def delete_data(self, nick):
        success = False
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            delete = """DELETE FROM users WHERE nick = ?"""

            cur.execute(delete, (nick,))
            print("[%s] User %s data deleted successfully" % (self.name, nick))
            success = True
        except sqlite3.Error as error:
            print("[%s] ERROR: Error deleting data from table users\n" % self.name, error)
        finally:
            if con:
                con.commit()
                con.close()
        return success

    def get_by_status(self, status, negated=False):
        users = []
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            sql_select_query = """SELECT * FROM users WHERE status = ?"""
            if negated:
                sql_select_query = """SELECT * FROM users WHERE status != ?"""
            cur.execute(sql_select_query, (status,))

            users = cur.fetchall()

            if not users:
                print("[DATABASE] INFO: Queried users with status %s, but none found" % status)

        except sqlite3.Error as error:
            print("[DATABASE] ERROR: Error reading data from table users\n", error)
        finally:
            if con:
                con.commit()
                con.close()

        return users

    def create_game(self, host, players):
        success = False
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            insert = """INSERT INTO games
                                     (host_nick, players, status, winner) 
                                     VALUES (?, ?, ?, NULL);"""
            cur.execute(insert, (host, players, GameStatus.RUNNING.value))

            success = True

        except sqlite3.Error as error:
            print("[DATABASE] ERROR: Error saving data in table games\n", error)
        finally:
            if con:
                con.commit()
                con.close()

        return success

    def update_game(self, host, status, winner):
        success = False
        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            insert = """UPDATE games SET
                                       status = ?, winner = ? WHERE host_nick = ?"""

            data_tuple = (status, winner, host)
            cur.execute(insert, data_tuple)
            print("[DATABASE] Game from host %s data updated successfully" % host)
            success = True
        except sqlite3.Error as error:
            print("[DATABASE] ERROR: Error updating data from table games\n", error)
        finally:
            if con:
                con.commit()
                con.close()

        return success
