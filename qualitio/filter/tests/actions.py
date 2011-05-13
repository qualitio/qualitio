# -*- coding: utf-8 -*-
from nose.tools import *
from qualitio.core.tests.utils import BaseTestCase
from qualitio.filter import actions as filteractions


class ActionImportingTest(BaseTestCase):
    def test_finds_all_actions(self):
        actions = filteractions.find_actions('qualitio.filter')
        assert filteractions.Action in actions, '%s should be in actions' % filteractions.Action
        assert filteractions.DeleteAction in actions, '%s should be in actions' % filteractions.DeleteAction
