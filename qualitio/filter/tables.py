import django_tables as tables


def unique_list(*sequences):
    checked = []
    for seq in sequences:
        for e in seq:
            if e not in checked:
                checked.append(e)
    return checked


class ModelTable(tables.ModelTable):
    fields_order = []

    def __init__(self, *args, **kwargs):
        self.fields_order = kwargs.pop('fields_order', self.__class__.fields_order)
        self.base_columns.keyOrder = unique_list(
            self.fields_order,
            self.base_columns.keyOrder)
        super(ModelTable, self).__init__(*args, **kwargs)
