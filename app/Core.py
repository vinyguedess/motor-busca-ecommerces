from os import path, environ
import psycopg2


class Connection():

    _conn = None

    def __init__(self, host, dbname, user, passw):
        self._conn = psycopg2.connect(host=host, database=dbname, user=user, password=passw)

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def getConn(self):
        return self._conn.cursor()


class Config:

    _loadedDotEnv = False
    _data = {}

    def get(key, defaultValue=None):
        if not Config._loadedDotEnv:
            Config.loadDotEnv()

        if key in Config._data:
            return Config._data[key]

        if key in environ:
            return environ[key]

        return defaultValue

    def set(key, value):
        Config._data[key] = value

    def loadDotEnv():

        if not path.isfile('.env'):
            return None
        
        dot_env = open('.env', 'r')
        for line in dot_env.readlines():
            if line == '\n' or line[0] == '#':
                continue

            key, value = line.split('=')
            Config._data[key] = value.replace('\n', '')
            Config._data[key.lower().replace('_', '.')] = value.replace('\n', '')

        dot_env.close()

        Config._loadedDotEnv=True


class ErrorsManager():

    _errors = []

    def addError(self, message):
        self._errors.append(message)

    def getErrors(self):
        return self._errors

    def hasErrors(self):
        return len(self._errors) > 0