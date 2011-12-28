# -*- coding: utf-8 -*-
"""
Filter customization for charts purposes.
"""
from django import forms
from django.db.models import Q

from qualitio import filter as filterapp
from qualitio.store.models import TestCase
from qualitio.execute.models import TestRun


class UsedInTestRun(filterapp.FieldFilterForm):
    def __init__(self, *args, **kwargs):
        self.base_fields['q'] = forms.ModelChoiceField(
            queryset=TestRun.objects.all(),
            required=False
        )
        super(UsedInTestRun, self).__init__(*args, **kwargs)

    # - it's important to set this as not-required,
    # - "q" will be the TestRun object
    # - should be set up on TestCase objects filter

    # get the Q object with the specified query
    # note that you're writting Q for Requirement QuerySet
    def construct_Q(self):
        # Instances of this class will filter store.TestCase set.
        # We want to filter testcase that has testcaseruns in
        # the given testrun
        testrun = self.cleaned_data['q']
        return Q(testcaserun__parent=testrun) if testrun else Q()


class TestCaseFilter(filterapp.ModelFilter):
    class Meta:
        model = TestCase
        exclude=('lft', 'rght', 'tree_id', 'level', 'project')

    used_in_testrun = filterapp.FieldFilter(UsedInTestRun, label=u"Used in testrun")
