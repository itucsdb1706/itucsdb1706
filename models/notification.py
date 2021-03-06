import psycopg2 as dbapi2
from flask import current_app


class Notification:
    """ Blueprint of NOTIFICATION table """

    fields = ['notification_id', 'user_id', 'content', 'is_read']

    def __init__(self, notification_id, user_id, content, is_read=False):
        self.notification_id = notification_id
        self.user_id = user_id
        self.content = content
        self.is_read = is_read;

    def save(self):
        """
        Inserts notification into database.
        :return: None
        """
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """INSERT INTO NOTIFICATION (user_id, content, is_read) VALUES (%s, %s, %s)
                        RETURNING notification_id;"""
            cursor.execute(query, [self.user_id, self.content, self.is_read])
            self.notification_id = cursor.fetchone()[0]
            connection.commit()

    def delete(self):
        """
        Deletes notification from database.
        :return: None
        """
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM DISCUSSION WHERE discussion_id = %s;"""
            cursor.execute(query, self.discussion_id)
            connection.commit()

    def update(self):
        """
        Updates notification in database.
        :return: None
        """
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """UPDATE DISCUSSION SET user_id = %s, content  = %s, is_read = %s WHERE notification_id=%s;"""
            cursor.execute(query, (self.user_id, self.content, self.is_read, self.notification_id))
            connection.commit()

    @staticmethod
    def create():
        """
        Creates NOTIFICATION table in database.
        :return: None
        """
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """CREATE TABLE IF NOT EXISTS NOTIFICATION (
                                  notification_id    SERIAL PRIMARY KEY NOT NULL,
                                  user_id            INTEGER REFERENCES USERS(user_id) ON DELETE CASCADE NOT NULL,
                                  content            VARCHAR(1024),
                                  is_read            BOOLEAN
                                  );"""
            cursor.execute(statement)
            cursor.close()

    @staticmethod
    def get(**kwargs):
        """
        Queries notifications from database according to given arguments.
        :param kwargs: Arguments
        :return: list
        """
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """SELECT {} FROM NOTIFICATION WHERE ( {} ) ORDER BY notification_id DESC;""" \
                .format(', '.join(Notification.fields), 'AND '.join([key + ' = %s' for key in kwargs]))
            cursor.execute(statement, tuple(str(kwargs[key]) for key in kwargs))
            result = cursor.fetchall()
            # TODO: None check
            connection.commit()
            return [Notification.object_converter(row) for row in result]

    @staticmethod
    def get_all():
        """
        Gets all notifications from database.
        :return: list
        """
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT {} FROM NOTIFICATION;""".format(', '.join(Notification.fields))
            cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            return result

    @staticmethod
    def object_converter(values):
        """
        Creates a Notification object with given arguments.
        :param values: Objects attributes(tuple)
        :return: Team
        """

        notif = Notification('a', 'b', 'c')

        for ind, field in enumerate(Notification.fields):
            notif.__setattr__(field, values[ind])

        return notif

    @staticmethod
    def drop():
        """
        Drops NOTIFICATION table.
        :return: None
        """
        with dbapi2.connect(current_app.config['dsn']) as connection:
            cursor = connection.cursor()
            statement = """DROP TABLE  IF EXISTS NOTIFICATION CASCADE;"""
            cursor.execute(statement)
            cursor.close()
