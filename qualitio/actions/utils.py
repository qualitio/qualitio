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
