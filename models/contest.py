import psycopg2 as dbapi2
from flask import current_app


class Contest:
    fields = ['contest_id', 'contest_name', 'is_individual', 'start_time', 'end_time']

    def __init__(self, contest_name=None, is_individual=None, start_time=None, end_time=None):
        self.contest_id = None
        self.contest_name = contest_name
        self.is_individual = is_individual
        self.start_time = start_time
        self.end_time = end_time

    def save(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """INSERT INTO CONTEST (contest_name, is_individual, start_time, end_time) 
                                  VALUES (%s, %s, %s, %s);"""
            cursor.execute(statement, (self.contest_name,
                                       self.is_individual,
                                       self.start_time,
                                       self.end_time))
            self.contest_id = cursor.fetchone()[0]
            cursor.close()

    def delete(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DELETE FROM CONTEST 
                                  WHERE (contest_id = %s);"""
            cursor.execute(statement, (self.contest_id,))
            cursor.close()

    def update(self):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """UPDATE CONTEST
                                  SET contest_name = %s, is_individual = %s, start_time = %s, end_time = %s
                                  WHERE (contest_id = %s);"""
            cursor.execute(statement, (self.contest_name,
                                       self.is_individual,
                                       self.start_time,
                                       self.end_time,
                                       self.contest_id))
            cursor.close()

    @staticmethod
    def create():
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """CREATE TABLE IF NOT EXISTS CONTEST (
                                  contest_id    SERIAL PRIMARY KEY NOT NULL,
                                  contest_name  VARCHAR(256) NOT NULL,
                                  is_individual BOOLEAN NOT NULL,
                                  start_time    TIMESTAMP NOT NULL,
                                  end_time      TIMESTAMP NOT NULL 
                                  );"""
            cursor.execute(statement)
            cursor.close()

    @staticmethod
    def get(*args, **kwargs):
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            where_cond = ' '.join([key + ' = ' + str(kwargs[key]) for key in kwargs])
            statement = """SELECT * FROM CONTEST WHERE (""" + where_cond + """);"""
            cursor.execute(statement)
            result = cursor.fetchall()
            cursor.close()
            return [Contest.object_converter(item) for item in result]

    @staticmethod
    def get_all():
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT * FROM CONTEST;"""
            cursor.execute(statement)
            result = cursor.fetchall()
            cursor.close()
            return result

    @staticmethod
    def object_converter(values):
        contest = Contest()

        for ind, field in enumerate(Contest.fields):
            contest.__setattr__(field, values[ind])

        return contest
