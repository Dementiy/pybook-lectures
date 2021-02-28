def attrs(obj):
    return {field.name: getattr(obj, field.name) for field in obj.fields}
