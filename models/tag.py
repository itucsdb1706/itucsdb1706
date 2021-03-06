import psycopg2 as dbapi2
from flask import current_app


class Tag:
    fields = ['tag_id', 'tag_name']

    def __init__(self, tag_name=None, tag_id=None):
        self.tag_id = tag_id
        self.tag_name = tag_name

    def save(self):
        """Saves this tag object to the database, also assigns the id of the message in the database to the object"""
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """INSERT INTO TAG (tag_name) 
                                  VALUES (%s) 
                                  RETURNING tag_id;"""
            cursor.execute(statement, (self.tag_name,))
            self.tag_id = cursor.fetchone()[0]
            cursor.close()

    def delete(self):
        """Deletes this tag inside the database by using its id"""
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM TAG 
                                  WHERE (tag_id = %s);"""
            cursor.execute(statement, (self.tag_id,))
            cursor.close()

    def update(self):
        """Updates the entire tag row with this objects values"""
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """UPDATE TAG 
                                  SET tag_name = %s 
                                  WHERE (tag_id = %s);"""
            cursor.execute(statement, (self.tag_name, self.tag_id))
            cursor.close()

    @staticmethod
    def create():
        """Executes the create statement for the TAG table in the database"""
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """CREATE TABLE IF NOT EXISTS TAG (
                                  tag_id    SERIAL PRIMARY KEY NOT NULL,
                                  tag_name  VARCHAR(64) NOT NULL
                                  );"""
            cursor.execute(statement)
            cursor.close()

    @staticmethod
    def get(**kwargs):
        """Generic get command with flexible arguments for tag fetching from the database
            :returns list of fetched tag objects"""
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT {} FROM TAG WHERE ( {} );""" \
                .format(', '.join(Tag.fields), 'AND '.join([key + ' = %s' for key in kwargs]))
            cursor.execute(statement, tuple(str(kwargs[key]) for key in kwargs))
            result = cursor.fetchall()
            connection.commit()
            return [Tag.object_converter(row) for row in result]

    @staticmethod
    def get_all(**kwargs):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT {} FROM TAG ORDER BY tag_name;""".format(', '.join(Tag.fields))
            cursor.execute(statement, tuple(str(kwargs[key]) for key in kwargs))
            result = cursor.fetchall()
            connection.commit()
            return [Tag.object_converter(row) for row in result]

    @staticmethod
    def object_converter(values):
        """Generic tag object conversion method for converting the tuples returned from select statements
            :returns tag object that wraps the values in the tuple list"""
        tag = Tag()

        for ind, field in enumerate(Tag.fields):
            tag.__setattr__(field, values[ind])

        return tag

    @staticmethod
    def drop():
        """Executes the drop statement to the TAG table"""
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DROP TABLE IF EXISTS TAG CASCADE;"""
            cursor.execute(statement)
            cursor.close()
