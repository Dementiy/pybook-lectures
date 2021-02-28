import sqlite3


def _access_fields_by_name(cursor, row):
    header = [field[0].lower() for field in cursor.description]
    return dict(zip(header, row))


class SQLiteDatabase:
    def __init__(self, database: str) -> None:
        self.database = database
        self._connection = None
        self.connected = False

    @property
    def connection(self):
        if self.connected:
            return self._connection
        self._connection = sqlite3.connect(self.database)
        self._connection.row_factory = _access_fields_by_name
        self.connected = True
        return self._connection

    def close(self):
        if self.connected:
            self.connection.close()
        self.connected = False

    def commit(self):
        self.connection.commit()

    def execute(self, sql, *args):
        return self.connection.execute(sql, args)

    def executescript(self, script):
        self.connection.cursor().executescript(script)
        self.commit()
