# -*- coding: utf-8 -*-
from django import template


register = template.Library()


class TableNode(template.Node):
    def __init__(self, table_class_name, data_name, var_name):
        self.table_class_name = table_class_name
        self.data_name = data_name
        self.var_name = var_name

    def render(self, context):
        table_class = template.Variable(self.table_class_name).resolve(context)
        data = template.Variable(self.data_name).resolve(context)
        table = table_class.__class__(data)
        context[self.var_name] = table
        return u""


def create_table(parser, token):
    """
    {% create_table TableClass data as <var_name> %}
    """
    _, TableClassID, DataID, _, VarNameID = range(5)
    parts = token.split_contents()

    if len(parts) < 5:
        raise template.TemplateSyntaxError("'table' tag must be of the form: {% create_table TableClass data as <var_name> %}")
    return TableNode(parts[TableClassID], parts[DataID], parts[VarNameID])

register.tag('create_table', create_table)
