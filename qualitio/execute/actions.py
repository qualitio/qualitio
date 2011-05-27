from qualitio.filter import actions
from qualitio.execute.models import TestRun

class ChangeParent(actions.ChangeParent):
    model = TestRun
