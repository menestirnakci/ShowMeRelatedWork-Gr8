import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
            """ 
            CREATE TABLE IF NOT EXISTS ADMINS
            (
                UserName VARCHAR(10) NOT NULL,
                ID serial ,
                UserPassword VARCHAR(16) NOT NULL,
                PRIMARY KEY (ID)
            )
            """,
            """ 
            CREATE TABLE IF NOT EXISTS Users
            (
                ID serial,
                Name VARCHAR(10) NOT NULL,
                Surname VARCHAR(10) NOT NULL,
                Gender VARCHAR(8) NOT NULL,
                UserName VARCHAR(10) NOT NULL UNIQUE,
                Password VARCHAR(256) NOT NULL,
                PRIMARY KEY (ID)
            )
            """,
            """ 
            CREATE TABLE IF NOT EXISTS Followed
            (
                ID serial,
                Source VARCHAR(10) NOT NULL,
                Target VARCHAR(10) NOT NULL,
                PRIMARY KEY (ID)
            )
            """,
            """ 
            CREATE TABLE IF NOT EXISTS About
            (
                ID serial,
                username VARCHAR(10) NOT NULL UNIQUE,
                info VARCHAR(500) NOT NULL,
                PRIMARY KEY (ID)
            )
            """,

            """ 
            CREATE TABLE IF NOT EXISTS Bookmarks
            (
                ID serial,
                username VARCHAR(10) NOT NULL,
                url VARCHAR(250) NOT NULL,
                PRIMARY KEY (ID)
            )
            """
            
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("url")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
