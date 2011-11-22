from qualitio.core.utils import json_response, failed
from qualitio.actions.base import find_actions


@json_response
def actions(request, app_label=None, action_name=None, **kwargs):
    allactions = find_actions('qualitio.%s' % app_label)
    for action_class in allactions:
        action = action_class(data=request.POST, request=request)
        if action.name == action_name:
            return action.execute()
    return failed(message="Wrong request")
