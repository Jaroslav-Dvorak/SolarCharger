import psycopg2
from psycopg2.extras import RealDictCursor


class Database:
    def __init__(self, conn_data):
        self._conn = psycopg2.connect(**conn_data)
        self._cursor = self._conn.cursor(cursor_factory=RealDictCursor)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()


class SqlWriter:
    def __init__(self, conn_data):
        self.conn_data = conn_data
        with Database(conn_data) as db:
            result = db.query(f"SELECT * FROM StationParameters")
            self.parameters = {r["name"].lower(): r["id"] for r in result}

    def write_values(self, values):
        string_1 = "INSERT INTO StationData(stationid, parameterid, value) VALUES"
        string_2 = ""
        for k, v in values.items():
            if string_2:
                string_2 += ", "
            string_2 += f"(1, {self.parameters[k.lower()]}, {v})"
        with Database(self.conn_data) as db:
            db.execute(string_1 + string_2)
