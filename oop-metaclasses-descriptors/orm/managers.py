from .fields import CharField, IntegerField
from .query import QuerySet
from .utils import attrs

DATA_TYPES = {
    CharField: "TEXT",
    IntegerField: "INTEGER",
}


def render_column_definitions(model):
    return ["%s %s" % (field.name, DATA_TYPES[type(field)]) for field in model.fields]


def render_create_table_stmt(model):
    sql = "CREATE TABLE {table_name} (id INTEGER PRIMARY KEY, {column_def});"
    column_definitions = ", ".join(render_column_definitions(model))
    params = {"table_name": model.__tablename__, "column_def": column_definitions}
    print(f"DEBUG: {sql.format(**params)}")
    return sql.format(**params)


class Manager:
    def __init__(self, db, model):
        self.db = db
        self.model = model
        self.table_name = self.model.__tablename__
        if not self._hastable():
            self.db.executescript(render_create_table_stmt(self.model))

    def get_queryset(self) -> QuerySet:
        return QuerySet(self.db, self.model)

    def all(self) -> QuerySet:
        return self.get_queryset()

    def get(self, id):
        return self.all().get(id)

    def order_by(self, *fields) -> QuerySet:
        return self.all().order_by(*fields)

    def filter(self, criteria) -> QuerySet:
        return self.all().filter(criteria)

    def save(self, obj) -> None:
        if obj.pk:
            self._update(obj)
        else:
            self._save(obj)

    def _save(self, obj) -> None:
        fields = attrs(obj)
        column_names = ", ".join(fields.keys())
        column_references = ", ".join("?" for i in range(len(fields)))
        sql = f"INSERT INTO {self.table_name} ({column_names}) VALUES ({column_references})"
        print(f"DEBUG: {sql}")
        cursor = self.db.execute(sql, *fields.values())
        obj.id = cursor.lastrowid

    def _update(self, obj) -> None:
        fields = attrs(obj)
        expressions = ", ".join(f"{field}=?" for field in fields)
        sql = f"UPDATE {self.table_name} SET {expressions} WHERE id=?"
        print(f"DEBUG: {sql}")
        self.db.execute(sql, *fields.values(), obj.pk)

    def delete(self):
        return self.all().delete()

    def _hastable(self) -> bool:
        # @see: https://stackoverflow.com/a/1604121
        sql = f"SELECT COUNT(*) FROM sqlite_master WHERE type=? AND name=? COLLATE NOCASE"
        cursor = self.db.execute(sql, "table", self.table_name)
        [(_, exists)] = cursor.fetchone().items()
        return bool(exists)
