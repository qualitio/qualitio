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

    def __init__(self, *args, **kwargs):
        self.query_dict = kwargs.pop('query_dict', {})
        self.fields_order = kwargs.pop('fields_order', self.__class__.fields_order)
        self.base_columns = custom_fields_columns(self._meta.model, self.base_columns)
        self.base_columns.keyOrder = unique_list(
            ['checkbox'],
            self.fields_order,
            self.base_columns.keyOrder)
        super(ModelTable, self).__init__(*args, **kwargs)

    checkbox = tables.Column(verbose_name="  ")

    def render_checkbox(self, instance):
        is_checked = self.query_dict.get('item-%s' % instance.id) == 'on'
        widget = '<input class="table-item" name="item-%s" type="checkbox" %s/>'
        widget = widget % (instance.id, 'checked' if is_checked else '')
        return mark_safe(widget)

    def get_absolute_url(self, objid):
        return u'/%(app_name)s/#%(model_name)s/%(id)s/details/' % {
            'id': objid,
            'app_name': self._meta.model._meta.app_label,
            'model_name': self._meta.model.__name__.lower(),
            }

    def link(self, id, label):
        return mark_safe(u'<a href="%(href)s">%(label)s</a>' % {
            'href': self.get_absolute_url(id),
            'label': label,
            })

    def render_id(self, obj):
        return self.link(obj.id, obj.id)

    def render_path(self, obj):
        if not obj.parent:
            return obj.path
        return self.link(obj.parent.id, obj.path)

    def render_name(self, obj):
        return self.link(obj.id, obj.name)

    def __unicode__(self):
        return u''


def generate_model_table(model, fields=None, exclude=(), fields_order=()):
    Model = model
    fields_to_include = fields
    fields_to_exclude = exclude
    new_fields_order = fields_order

    class _ModelTable(ModelTable):
        fields_order = new_fields_order

        class Meta:
            model = Model
            fields = fields_to_include
            exclude = fields_to_exclude

    return _ModelTable
