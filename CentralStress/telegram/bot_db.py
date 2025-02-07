import sqlite3
from dotenv import dotenv_values
import argparse
import logging

config = dotenv_values(".env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DATABASE_PATH = "C:\\Users\\User14\\PycharmProjects\\CentralStress\\database\\people.db"


def delete_user(user_id: int):
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM Users WHERE user_id = ?', (user_id,))
        connection.commit()


def get_vibe(user_id):
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT vibe FROM Users WHERE user_id = ?', (user_id,))
        result = cursor.fetchall()
    return result[0][0]


def add_user(user_id, name):
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Users (user_id, name, vibe) VALUES (?, ?, ?)", (int(user_id), str(name), ""))
        connection.commit()


def create_db():
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY,user_id INTEGER NOT NULL, name TEXT NOT NULL, vibe TEXT NOT NULL)")
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_id ON Users (user_id) ')
        connection.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Добавление в список пользователей бота")
    parser.add_argument("--command", help="Команда. 1 добавить, 0 удалить", type=int, default=1)
    parser.add_argument("--user_id", help="Id пользователя", type=int)
    args = parser.parse_args()
    if args.command == 1:
        add_user(args.user_id, args.status)
    elif args.command == 0:
        delete_user(args.user_id)
    # python
