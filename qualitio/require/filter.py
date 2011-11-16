# -*- coding: utf-8 -*-
# Simple customization to qualitio filter application
# it simply shows how to add extra filter
from django import forms
from django.db.models import Q

from qualitio import filter as filterapp
from qualitio.require.models import Requirement
from qualitio.store.models import TestCase


# This is implementation of filter can show all requirements that are / aren't related to any testcase
class IsAssignedToTestCaseFilterForm(filterapp.FieldFilterForm):
    q = forms.NullBooleanField(required=False)  # it's important to set this as not-required

    def __init__(self, *args, **kwargs):
        self.base_fields['q'].widget.choices = (
            (u'1', '-----------'),  # default "Unknown" label doesn't fit here
            (u'2', 'Yes'),
            (u'3', 'No'),
            )
        super(IsAssignedToTestCaseFilterForm, self).__init__(*args, **kwargs)

    # get the Q object with the specified query
    # note that you're writting Q for Requirement QuerySet
    def construct_Q(self):
        value = self.cleaned_data['q']

        if value == True:
            # show all requirements that ARE related to any testcase
            qs = Q(testcase__in=TestCase.objects.filter(requirement__isnull=False))
        elif value == False:
            # show all requirements that AREN'T related to any testcase
            qs = Q(testcase__isnull=True)
        else:
            # by default it's only the empty query
            qs = Q()

        return qs


# Another example
class IsAssignedToTestCaseThatHasStepsFilterForm(filterapp.FieldFilterForm):
    q = forms.NullBooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.base_fields['q'].widget.choices = (
            (u'1', '-----------'),
            (u'2', 'is assigned to TC with steps'),
            (u'3', 'is assigned to TC without steps'),
            )
        super(IsAssignedToTestCaseThatHasStepsFilterForm, self).__init__(*args, **kwargs)

    def construct_Q(self):
        value = self.cleaned_data['q']

        if value == True:
            qs = Q(testcase__in=TestCase.objects.filter(requirement__isnull=False, steps__isnull=False))
        elif value == False:
            qs = Q(testcase__in=TestCase.objects.filter(requirement__isnull=False, steps__isnull=True))
        else:
            qs = Q()

        return qs


class RequirementFilter(filterapp.ModelFilter):
    class Meta:
        model = Requirement
        exclude=('lft', 'rght', 'tree_id', 'level')

    is_assigned_to_testcase = filterapp.FieldFilter(IsAssignedToTestCaseFilterForm,
                                                    label='Is assigned to TC')

    is_assigned_to_testcase_with_steps = filterapp.FieldFilter(IsAssignedToTestCaseThatHasStepsFilterForm,
                                                               label='Requirement')
