from __future__ import annotations

import typing as tp

if tp.TYPE_CHECKING:
    from .models import Model


class QuerySet:
    def __init__(self, db, model) -> None:
        self.db = db
        self.model = model
        self.table_name = self.model.__tablename__
        self.sql = f"SELECT * FROM {self.table_name}"

    def __iter__(self):
        print(f"DEBUG: execute query: {self.sql}")
        cursor = self.db.execute(self.sql)
        return iter(self.model(**row) for row in cursor.fetchall())

    def get(self, id) -> Model:
        q = self.filter(f"id={id}")
        cursor = self.db.execute(self.sql)
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"Object `{self.model.__name__}` with id {id} does not exists")
        return self.model(**row)

    def order_by(self, *fields) -> QuerySet:
        order = ", ".join(fields)
        self.sql = f"{self.sql} ORDER BY {order}"
        return self

    def filter(self, criteria) -> QuerySet:
        key_word = "AND" if "WHERE" in self.sql else "WHERE"
        self.sql = f"{self.sql} {key_word} {criteria}"
        return self

    def delete(self):
        sql = f"DELETE FROM {self.table_name} WHERE id IN (SELECT id FROM ({self.sql}))"
        self.db.execute(sql)
