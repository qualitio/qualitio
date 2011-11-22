from django import forms

from qualitio.require import models
from qualitio import actions


class ChangeParent(actions.ChangeParent):
    model = models.Requirement
