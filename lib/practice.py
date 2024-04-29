from . import CONN
from . import CURSOR

class Movie:
    def __init__(self, title:str, year:int, id:int=None):
        self.id = id
        self.title = title
        self.year = year

    def __repr__(self):
        return f'Movie(id={self.id}, title={self.title}, year={self.year})'


    # --- SQL CLASS METHODS --- #

    @classmethod
    def create_table(cls):
        sql='''CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY,
        title TEXT,
        year INTEGER
        ) '''
        # creates the table if it doesn't exist
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def get_all(cls):
        sql= '''SELECT * FROM movies '''
        # creates a new instance for each row in the db
        read_all_tuples = CURSOR.execute(sql).fetchall()

        all_movies = []

        for tup in read_all_tuples:
            movie = Movie(title=tup[1], year=tup[2], id=tup[0])
            all_movies.append(movie)

        return all_movies

    @classmethod
    def get_by_id(cls, id:int):
        sql='''SELECT * FROM courses WHERE id = ? '''

        found_movie_tuple = CURSOR.execute(sql, [ id ]).fetchone()
        
        if found_movie_tuple:
            return Movie(title=found_movie_tuple[1], year=found_movie_tuple[2], id=found_movie_tuple[0])

        # finds by id and if found instantiates a new instance


    # --- SQL INSTANCE METHODS --- #

    def create(self):
        sql='''INSERT INTO movies ( title )
        VALUES ( ?, ? ) 
        '''

        CURSOR.execute(sql, [self.title, self.year])
        CONN.commit()

        last_row_sql = 'SELECT * FROM movies ORDER BY id DESC LIMIT 1'
        last_row_tuple = CURSOR.execute(last_row_sql).fetchone()
        # creates in the db and updates instance with the new id

        self.id = last_row_tuple[0]


    def update(self):
        sql='''UPDATE courses 
        SET title = ?, year = ?
        WHERE id = ?
        '''
        # updates the row based on current attributes 
        CURSOR.execute(sql, [self.title, self.year, self.id])
        CONN.commit()

    def save(self):
        if not self.id:
            self.create()
        # creates if it doesn't exist
        # updates if it does exist
        else:
            self.update()

    
    def destroy(self):
        sql='''DELETE FROM movies WHERE id = ?'''

        CURSOR.execute(sql, [self.id])
        CONN.commit()

        self.id = None
        # deletes the instance from the db and removes the id