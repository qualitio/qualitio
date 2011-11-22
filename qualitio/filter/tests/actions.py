# -*- coding: utf-8 -*-
from nose.tools import *
from qualitio.core.tests.utils import BaseTestCase
from qualitio import actions as filteractions

from qualitio.filter.tests.testapp import models
from qualitio.filter.tests.testapp.actions import ChangeFileParent, ChangeDirectoryParent


class ActionImportingTest(BaseTestCase):
    def setUp(self):
        self.addTestApps(['qualitio.filter.tests.testapp'])

    def test_finds_all_actions(self):
        actions = filteractions.find_actions('qualitio.filter.tests.testapp')
        assert ChangeFileParent in actions, '%s should be in actions' % ChangeFileParent
        assert ChangeDirectoryParent in actions, '%s should be in actions' % ChangeDirectoryParent

    def test_finds_action_only_for_given_model(self):
        files_only = filteractions.find_actions('qualitio.filter.tests.testapp', model=models.File)
        assert ChangeFileParent in files_only, '%s should be in actions' % ChangeFileParent
        assert ChangeDirectoryParent not in files_only, '%s SHOULDN\'T be in actions' % ChangeDirectoryParent
