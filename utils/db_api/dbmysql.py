import mysql.connector
from data.config import *

class DataBase():
    def update_connection(self):
        self.cursor.close()
        self.con.close()
        self.__init__()

    def __init__(self) -> None:
        self.con = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            database=DB_NAME,
            password=DB_PASS,
            charset="utf8mb4",
            autocommit=True)
        self.cursor = self.con.cursor(buffered=True)

    def new_user(self,user_id):
        self.update_connection()
        cursor=self.cursor
        cursor.execute("INSERT IGNORE INTO users (tg_id) VALUES(%s)",(user_id,))
        return cursor.lastrowid

    def user(self,user_id):
        self.update_connection()
        cursor=self.cursor
        cursor.execute("SELECT * FROM users WHERE tg_id=%s",(user_id,))
        user=cursor.fetchall()
        return user

    def stat_bot(self):
        self.update_connection()
        cursor=self.cursor
        cursor.execute("SELECT (SELECT COUNT(*) FROM users WHERE DATE(date_start) >= DATE_SUB(NOW(), INTERVAL 1 MONTH)),"
    "(SELECT COUNT(*) FROM users WHERE DATE(date_start) >= DATE_SUB(NOW(), INTERVAL 1 DAY))")
        users=cursor.fetchall()
        return users

