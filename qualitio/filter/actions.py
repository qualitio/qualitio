# -*- coding: utf-8 -*-
import re
from qualitio.core.utils import success, failed
from qualitio.core.forms import BaseForm


class Action(object):
    item_id_ptr = re.compile(r'^item-(?P<id>\d+)$')
    model = None
    action_form_class = None
    name = 'action'
    label = 'Action'

    def queryset(self):
        result = []
        for key in self.data.keys():
            match = self.item_id_ptr.match(key)
            if match:
                result.append(int(match.group('id')))
        return self.model.objects.filter(id__in=result)

    def execute(self, request):
        return success(success=True, message='Action validation OK')


class DeleteAction(Action):
    name = 'delete'
    label = 'Delete'

    def run(self):
        queryset = self.queryset()
        # queryset.delete()
