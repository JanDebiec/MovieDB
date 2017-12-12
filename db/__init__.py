import sqlite3

sqlite_file = 'data/movie_db1.sqlite'    # name of the sqlite database file

sql_create_movies_table = """ CREATE TABLE IF NOT EXISTS movies (
                                    movieid integer PRIMARY KEY,
                                    ean text NOT NULL,
                                    imdbtitle text NOT NULL,
                                    origintitle text NOT NULL,
                                    localtitle text NOT NULL,
                                    imdbrating integer,
                                    userrating integer,
                                    source text NOT NULL,
                                    medium text NOT NULL,
                                    alreadyseen text NOT NULL,
                                    reserve text NOT NULL
                                ); """
