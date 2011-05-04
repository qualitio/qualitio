def get_db_field(Model, field_or_field_name_):
    field = field_or_field_name_
    if isinstance(field_or_field_name_, basestring):
        field = Model._meta.get_field(field_or_field_name_)
    return field


def camel_name(name):
    return ''.join([w.capitalize() for w in name.split('_')])


def class_field_name(name, base_name):
    return '%s%s' % (camel_name(name), base_name)


def pretty_field_name(name):
    return ' '.join(name.split('_')).capitalize()


class ObjectCounterMetaclass(type):
    """
    ObjectCounterMetaclass provides way to create class
    with creation counter that doesn't need to invoke
    __init__ method.
    """
    def __new__(cls, cls_name, bases, attrs):
        attrs['creation_counter'] = 0
        return type.__new__(cls, cls_name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj.creation_counter = obj.__class__.creation_counter
        obj.__class__.creation_counter += 1
        return obj


class ObjectCounter(object):
    __metaclass__ = ObjectCounterMetaclass
