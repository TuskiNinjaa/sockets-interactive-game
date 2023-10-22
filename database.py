import sqlite3


class DataBase:
    def __init__(self, db_path = None):
        self.db_path = db_path or "storage.db"

        self.__check_connection()

    def __check_connection(self):

        try:
            con = sqlite3.connect(self.db_path)
            cur = con.cursor()
            cur.execute(
                """SELECT * FROM users LIMIT 1""").fetchall()
        except sqlite3.OperationalError as error:
            print("[DATABASE] ERROR: Error reading data from table, trying to create it\n", error)
            self.__create_table(cur)
        except sqlite3.Error as error:
            print("[DATABASE] ERROR: Error reading data from table\n", error)
        finally:
            if con:
                con.commit()
                con.close()


    def __create_table(self, cur):
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
                pass
            insert = """INSERT INTO users
                         (username ,nick, password, status, ip, port) 
                         VALUES (?, ?, ?, ?, ?, ?);"""

            data_tuple = (username, nick, password, status, ip, port)
            cur.execute(insert, data_tuple)
            print("[DATABASE] User %s data saved successfully"%nick)
            success = True
        except sqlite3.Error as error:
            print("[DATABASE] ERROR: Error saving data from table\n", error)
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
            print("[DATABASE] User %s data saved successfully"% nick)
            success = True
        except sqlite3.Error as error:
            print("[DATABASE] ERROR: Error saving data from table\n", error)
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
            print("[DATABASE] User %s data updated successfully"%nick)
            success = True
        except sqlite3.Error as error:
            print("[DATABASE] ERROR: Error updating data from table\n", error)
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
            print("[%s] ERROR: Error deleting data from table\n" % self.name, error)
        finally:
            if con:
                con.commit()
                con.close()
        return success

    def get_by_status(self, status, negated = False):
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
            print("[DATABASE] ERROR: Error reading data from table\n", error)
        finally:
            if con:
                con.commit()
                con.close()

        return users