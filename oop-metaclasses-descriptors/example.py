from faker import Faker

from orm.database import SQLiteDatabase
from orm.fields import CharField
from orm.models import Model

db = SQLiteDatabase("temp_db.sqlite3")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    __tablename__ = "users"
    username = CharField()
    email = CharField()
    password = CharField()

    def __repr__(self):
        return f"User(id={self.pk}, username={self.username}, email={self.email})"


if __name__ == "__main__":
    fake = Faker()

    for _ in range(10):
        profile = fake.simple_profile()
        password = fake.password(length=12)
        user = User(username=profile["username"], email=profile["mail"], password=password)
        user.save()

    db.commit()
