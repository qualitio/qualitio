from nose.tools import *
from django.test import TestCase
from qualitio import store
import models


class RunTestCase(TestCase):
    def setUp(self):
        self.test_case_directory = store.TestCaseDirectory.objects.get(parent=None)
        self.test_case = store.TestCase.objects.create(name="test_name",
                                                       precondition="precondtion",
                                                       description="description",
                                                       parent=self.test_case_directory)

        self.test_run_directory = models.TestRunDirectory.objects.get(parent=None)
        self.test_run = models.TestRun.objects.create(name="name", parent=self.test_run_directory)


    def test_run_test_case(self):
        test_case_run = models.TestCaseRun.run(self.test_case, self.test_run)

        self.assertEqual(self.test_case.name, test_case_run.name)
        self.assertEqual(self.test_case.description, test_case_run.description)
        self.assertEqual(self.test_case.precondition, test_case_run.precondition)

        self.assertEqual(self.test_case.steps.count(),
                         test_case_run.steps.count())


    def test_run_test_case_with_steps(self):
        self.test_case.steps.create(description="step_1_description",
                                    expected="step_1_excpected",
                                    sequence=0)

        self.test_case.steps.create(description="step_2_description",
                                    expected="step_2_excpected",
                                    sequence=1)

        test_case_run = models.TestCaseRun.run(self.test_case, self.test_run)

        self.assertEqual(self.test_case.steps.count(),
                         test_case_run.steps.count())

        for test_case_step in self.test_case.steps.all():
            test_case_run_step = test_case_run.steps.get(sequence=test_case_step.sequence)
            self.assertEqual(test_case_step.description, test_case_run_step.description)
            self.assertEqual(test_case_step.expected, test_case_run_step.expected)
