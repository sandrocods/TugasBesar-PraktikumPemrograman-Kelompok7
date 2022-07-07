import sqlite3


class Database:
    def __init__(self, db):
        try:
            self.db = db
            self.conn = sqlite3.connect(db, check_same_thread=False)
            self.c = self.conn.cursor()
            print("Database connected ✅ ...")
        except sqlite3.Error as e:
            print(e)

    def check_connection(self):
        try:
            self.conn = sqlite3.connect(self.db, check_same_thread=False)
            self.c = self.conn.cursor()
            print("Database connected ✅ ...")
        except sqlite3.Error as e:
            print(e)

    def insert(self, table, fields, values):
        try:
            self.c.execute("INSERT INTO " + table + " (" + fields + ") VALUES (" + values + ")")
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)

    def update(self, table, fields, values, where):
        try:
            self.c.execute("UPDATE " + table + " SET " + fields + " = " + values + " WHERE id_telegram=" + where)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)


    def check_user(self, user_id):
        try:
            self.c.execute("SELECT * FROM user WHERE id_telegram = {}".format(user_id))
            return self.c.fetchall()
        except sqlite3.Error as e:
            print(e)

    def check_nim(self, nim):
        try:
            self.c.execute("SELECT * FROM user WHERE nim = '{}'".format(nim))
            return self.c.fetchall()

        except sqlite3.Error as e:
            print(e)

    def check_igracias(self, user_id):
        try:
            self.c.execute("SELECT * FROM igracias_login WHERE id_telegram = '{}'".format(user_id))
            return self.c.fetchall()
        except sqlite3.Error as e:
            print(e)

    def check_lms(self, user_id):
        try:
            self.c.execute("SELECT * FROM user WHERE id_telegram = '{}'".format(user_id))
            return self.c.fetchall()
        except sqlite3.Error as e:
            print(e)

    def check_notif_tugas(self, user_id):
        try:
            self.c.execute("SELECT * FROM schedule_task WHERE id_telegram = '{}'".format(user_id))
            return self.c.fetchall()
        except sqlite3.Error as e:
            print(e)

    def get_all_last_status_true(self):
        try:
            self.c.execute("SELECT id_telegram, last_status FROM schedule_task WHERE last_status = 1")
            return self.c.fetchall()
        except sqlite3.Error as e:
            print(e)