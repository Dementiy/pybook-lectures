import typing as tp


class Field:
    def __init__(self, default: tp.Any = None) -> None:
        self.default = default

    def __get__(self, instance, owner) -> tp.Any:
        return instance.__dict__.get(self.name, self.default)

    def __set__(self, instance, value) -> None:
        instance.__dict__[self.name] = value

    def __set_name__(self, instance, name) -> None:
        self.name = name


class CharField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"Field `{self.name}` must be a string, not {type(value).__name__}")
        super().__set__(instance, value)


class IntegerField(Field):
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f"Field `{self.name}` must be an integer, not {type(value).__name__}")
        super().__set__(instance, value)
