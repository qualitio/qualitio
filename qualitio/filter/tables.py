# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe

import django_tables as tables


def unique_list(*sequences):
    checked = []
    for seq in sequences:
        for e in seq:
            if e not in checked:
                checked.append(e)
    return checked

def custom_fields_columns(model, columns):
    if hasattr(model, '_customization_model'):
        # Support for custom attributes
        for f in model._customization_model._custom_meta.get_custom_fields():
            if f.name not in columns:
                columns[f.name] = tables.Column(name=f.name, data='customization__%s' % f.name)
    return columns


class ModelTable(tables.ModelTable):
    fields_order = []
    show_checkbox = True

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')  # can raise exception
        self.query_dict = kwargs.pop('query_dict', {})
        self.fields_order = kwargs.pop('fields_order', self.__class__.fields_order)
        self.show_checkbox = kwargs.pop('show_checkbox', self.__class__.show_checkbox)
        self.base_columns = custom_fields_columns(self._meta.model, self.base_columns)

        self.base_columns.keyOrder = unique_list(
            ['checkbox'],
            self.fields_order,
            self.base_columns.keyOrder)

        if not self.show_checkbox:
            del self.base_columns['checkbox']

        super(ModelTable, self).__init__(*args, **kwargs)

    checkbox = tables.Column(verbose_name="  ")

    def render_checkbox(self, instance):
        is_checked = self.query_dict.get('item-%s' % instance.id) == 'on'
        widget = '<input class="table-item" name="item-%s" type="checkbox" %s/>'
        widget = widget % (instance.id, 'checked' if is_checked else '')
        return mark_safe(widget)

    def get_absolute_url(self, objid, model_name):
        return u'/project/%(project_name)s/%(app_name)s/#%(model_name)s/%(id)s/details/' % {
            'id': objid,
            'app_name': self._meta.model._meta.app_label,
            'model_name': model_name,
            'project_name': self.request.project.slug,
            }

    def link(self, id, label, model_name):
        return mark_safe(u'<a href="%(href)s">%(label)s</a>' % {
            'href': self.get_absolute_url(id, model_name),
            'label': label,
            })

    def render_id(self, obj):
        return self.link(obj.id, obj.id, self._meta.model.__name__.lower())

    def render_path(self, obj):
        if not obj.parent:
            return obj.path
        return self.link(obj.parent.id, obj.path, obj.parent.__class__.__name__.lower())

    def render_name(self, obj):
        return self.link(obj.id, obj.name, self._meta.model.__name__.lower())

    def __unicode__(self):
        return u''


def generate_model_table(model, columns=None, exclude=(), fields_order=(), bases=(ModelTable,)):
    return type('_ModelTable', bases, {
        'fields_order': fields_order,
        'Meta': type('Meta', (), {
            'model': model,
            'columns': columns,
            'exclude': exclude,
        })
    })
