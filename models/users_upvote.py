import psycopg2 as dbapi2
from flask import current_app


class UsersUpvote:

    @staticmethod
    def create():
        """
        Creates USERS_UPVOTE table in database.
        :return: None
        """
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """CREATE TABLE IF NOT EXISTS USERS_UPVOTE (
                                  user_id       INTEGER REFERENCES USERS(user_id) ON DELETE CASCADE NOT NULL,
                                  discussion_id INTEGER REFERENCES DISCUSSION(discussion_id) ON DELETE CASCADE NOT NULL,
                                  PRIMARY KEY (user_id, discussion_id)
                                  );"""
            cursor.execute(statement)
            cursor.close()

    @staticmethod
    def upvote(user_id, discussion_id):
        """
        nserts (user_id, discussion_id) row into USERS_UPVOTE table
        :param user_id: int
        :param discussion_id: int
        :return: None
        """
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT user_id, discussion_id FROM USERS_UPVOTE
                            WHERE ( user_id = %s AND discussion_id = %s );"""
            cursor.execute(statement, (user_id, discussion_id))
            result = cursor.fetchall()
            cursor.close()

        if result:
            return

        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """UPDATE DISCUSSION SET upvote = upvote + 1 WHERE discussion_id = %s;"""
            cursor.execute(statement, (discussion_id,))
            cursor.close()

        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """INSERT INTO USERS_UPVOTE (user_id, discussion_id) VALUES (%s, %s);"""
            cursor.execute(statement, (user_id, discussion_id))
            cursor.close()

    @staticmethod
    def drop():
        """
        Drops USERS_UPVOTE table.
        :return: None
        """
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DROP TABLE  IF EXISTS USERS_UPVOTE CASCADE;"""
            cursor.execute(statement)
            cursor.close()