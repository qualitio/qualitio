from django.conf import settings
from django.utils.importlib import import_module


engine = None


def get_engine():
    global engine
    if not engine:
        engine = import_module(getattr(settings, 'CHART_TYPES_ENGINE'))
        engine.name = '%s-charttype' % engine.__name__.split('.')[-1]
    return engine
