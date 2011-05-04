# -*- coding: utf-8 -*-
from django.utils.datastructures import SortedDict
from django.core.exceptions import ImproperlyConfigured

from qualitio.filter.fieldfilters import (FieldFilter,
                                          fieldfilters_for_model,
                                          related_objects_filters_for_model)
from qualitio.filter import utils


class Options(object):
    def __init__(self, opts, object_name=None):
        self.fields = getattr(opts, 'fields', None)
        self.exclude = getattr(opts, 'exclude', None)
        self.model = getattr(opts, 'model', None)
        self.related_objects = getattr(opts, 'related_objects', False)
        self.object_name = object_name


def merge_meta_attributes(meta_classes, Meta=None, exclude=()):
    if not meta_classes:
        return None

    attrs = {}
    for meta in meta_classes:
        attrs.update(meta.__dict__)

    # let's remove things that we don't want to inherit
    for fname in exclude:
        if fname in attrs:
            del attrs[fname]

    if Meta:
        attrs.update(Meta.__dict__)

    return type.__new__(type, 'Meta', (), attrs)


class MetaFilter(type):
    """
    Filter metaclass
    """
    def __new__(cls, class_name, bases, attrs):
        # extract user defined fields
        declared_filters = [(name, attrs.pop(name))
                  for name, obj in attrs.items()
                  if isinstance(obj, FieldFilter)]
        declared_filters.sort(lambda x, y: cmp(x[1].creation_counter, y[1].creation_counter))

        # we'll collect also Meta classes to merge all of those options
        meta_classes = []

        # add fields from bases in proper order
        for base in bases[::-1]:
            declared_filters = getattr(base, 'base_filters', {}).items() + declared_filters
            meta = getattr(base, '_meta', None)
            if meta:
                meta_classes.append(meta)

        Meta = attrs.get('Meta')

        # converting to dict
        declared_filters = SortedDict(declared_filters)
        Meta = merge_meta_attributes(meta_classes, Meta)

        # getting meta attrinbutes
        opts = Options(Meta, object_name=class_name)

        base_filters = SortedDict()
        if opts.model:
            base_filters.update(fieldfilters_for_model(opts.model, fields=opts.fields, exclude=opts.exclude))

        if opts.model and opts.related_objects:
            base_filters.update(related_objects_filters_for_model(
                    opts.model, fields=opts.fields, exclude=opts.exclude))

        # override base_fields with whose which are defined by user
        base_filters.update(declared_filters)

        # setup name and model fieldfilter variables
        # for whose which were defined by user
        for name, fieldfilter in base_filters.items():
            fieldfilter.name = name
            fieldfilter.model = opts.model

        attrs['base_filters'] = base_filters
        attrs['_meta'] = opts
        new_class = type.__new__(cls, class_name, bases, attrs)

        return new_class
