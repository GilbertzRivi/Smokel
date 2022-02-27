from dotenv import load_dotenv
from sys import argv
from os import getenv
import sqlite3

load_dotenv('.env')

class Database:
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def create_table(self, sql: str):
        self.cursor.execute(sql)
        self.connection.commit()

    def insert(self, table, *values):
        self.cursor.execute(f'INSERT INTO {table} VALUES ({",".join(["?" for _ in values])})', values)
        self.connection.commit()

    def fetch(self, selector, table, condition):
        return self.cursor.execute(f'SELECT {selector} FROM {table} WHERE {condition}')

    def fetch_all(self, selector, table):
        return self.cursor.execute(f'SELECT {selector} FROM {table}')

    def delete(self, table, condition):
        self.cursor.execute(f'DELETE FROM {table} WHERE {condition}')
        self.connection.commit()

    def update(self, table, column, condition):
        self.cursor.execute(f'UPDATE {table} SET {column} WHERE {condition}')
        self.connection.commit()

if __name__ == '__main__':
    print('Creating database')
    db = Database(getenv('DB_NAME'))
    db.create_table("""CREATE TABLE IF NOT EXISTS black_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        banned_id INTEGER,
        description TEXT);
        """)
    db.create_table("""CREATE TABLE IF NOT EXISTS config (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        value INTEGR,
        grp TEXT);
        """)
    db.create_table("""CREATE TABLE IF NOT EXISTS veryfication (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGR,
        message_id INTEGR,
        join_time REAL);
        """)
    db.create_table("""CREATE TABLE IF NOT EXISTS counters (
        name TEXT PRIMARY KEY,
        value INTEGR);
        """)
    db.create_table("""CREATE TABLE IF NOT EXISTS autoroles (
        role_id INTEGR PRIMARY KEY,
        message_id INTEGR,
        channel_id INTEGR,
        is_excluded INTEGR);
        """)
    db.create_table("""CREATE TABLE IF NOT EXISTS invites (
        user_id INTEGR PRIMARY KEY,
        timestamp INTEGR);
        """)
    db.create_table("""CREATE TABLE IF NOT EXISTS mutes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGR,
        role INTEGR,
        timestamp INTEGR);
        """)