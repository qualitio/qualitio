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
    creation_counter = 0

    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj.creation_counter = ObjectCounterMetaclass.creation_counter
        ObjectCounterMetaclass.creation_counter += 1
        return obj


class ObjectCounter(object):
    __metaclass__ = ObjectCounterMetaclass



class Property(object):
    def __init__(self, target, default=lambda instance: None):
        self.name = target
        self.default_value = default

    def __get__(self, instance, type_instance):
        if instance is None:
            raise AttributeError('%s attribute can be get only on instance' % self.name)

        if not hasattr(instance, self.name):
            setattr(instance, self.name, self.default_value(instance))

        return getattr(instance, self.name)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)
