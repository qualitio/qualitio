from django import forms

from qualitio.require import models
from qualitio.filter import actions


class ChangeParent(actions.ChangeParent):
    model = models.Requirement
