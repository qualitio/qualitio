from django.utils.safestring import mark_safe

import django_tables

class FilterModelTable(django_tables.ModelTable):
    def __init__(self, *args, **kwargs):
        self.base_columns.keyOrder.pop(self.base_columns.keyOrder.index('checkbox'))
        self.base_columns.keyOrder = ['checkbox'] + self.base_columns.keyOrder
        self.query_dict = kwargs.pop('query_dict', {})
        super(FilterModelTable, self).__init__(*args, **kwargs)

    checkbox = django_tables.Column(verbose_name="  ")

    def render_checkbox(self, instance):
        is_checked = self.query_dict.get('item-%s' % instance.id) == 'on'
        widget = '<input class="table-item" name="item-%s" type="checkbox" %s/>'
        widget = widget % (instance.id, 'checked' if is_checked else '')
        return mark_safe(widget)


def generate_model_table(model, fields=None, exclude=()):
    model_, fields_, exclude_ = model, fields, exclude

    class ModelTable(FilterModelTable):
        class Meta:
            model = model_
            fields = fields_
            exclude = exclude_

    return ModelTable
