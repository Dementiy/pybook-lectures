from .fields import Field
from .managers import Manager
from .utils import attrs


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        # Во вновь создаваемый класс добавляем атрибут fields со
        # списком всех полей наследников от Field
        # TODO: В этом примере модели не поддерживают наследование полей
        new_cls = super().__new__(cls, name, bases, attrs)
        fields = []
        for field_name, field in attrs.items():
            if isinstance(field, Field):
                fields.append(field)
        new_cls.fields = fields
        return new_cls


class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for field_name, value in kwargs.items():
            setattr(self, field_name, value)

    def save(self):
        return self.__class__.manager().save(self)

    @classmethod
    def manager(cls, db=None) -> Manager:
        return Manager(db if db else cls.Meta.database, cls)

    @property
    def public(self):
        return attrs(self)

    @property
    def pk(self):
        if hasattr(self, "id"):
            return self.id
        return None
