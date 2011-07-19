from nose.tools import *
from django.test import TestCase
from qualitio import store
import models


class TestRunTestCase(TestCase):
    def setUp(self):
        self.test_case_directory = store.TestCaseDirectory.objects.create(parent=None,
                                                                          name="Root")
        self.test_case = store.TestCase.objects.create(name="test_name",
                                                       precondition="precondtion",
                                                       description="description",
                                                       parent=self.test_case_directory)

        self.test_run_directory = models.TestRunDirectory.objects.create(parent=None,
                                                                          name="Root")
        self.test_run = models.TestRun.objects.create(name="name", parent=self.test_run_directory)


    def test_run_test_case(self):

        test_case_run = self.test_run.run(self.test_case)

        # test_case_run = models.TestCaseRun.run(self.test_case, self.test_run)

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

        test_case_run = self.test_run.run(self.test_case)

        self.assertEqual(self.test_case.steps.count(),
                         test_case_run.steps.count())

        for test_case_step in self.test_case.steps.all():
            test_case_run_step = test_case_run.steps.get(sequence=test_case_step.sequence)
            self.assertEqual(test_case_step.description, test_case_run_step.description)
            self.assertEqual(test_case_step.expected, test_case_run_step.expected)



class TestBugshistory(TestCase):
    def setUp(self):
        self.test_case_directory = store.TestCaseDirectory.objects.create(parent=None,
                                                                          name="Root")

        self.test_case = store.TestCase.objects.create(name="test_case",
                                                       parent=self.test_case_directory)

        self.test_run_directory = models.TestRunDirectory.objects.create(parent=None,
                                                                          name="Root")
        self.test_run_1 = models.TestRun.objects.create(name="test_run_1",
                                                        parent=self.test_run_directory)

        self.test_run_2 = models.TestRun.objects.create(name="test_run_2",
                                                        parent=self.test_run_directory)

        self.test_case_run_1 = self.test_run_1.run(self.test_case)
        self.test_case_run_2 = self.test_run_2.run(self.test_case)


    def test_bugs_history(self):
        bug_1 = self.test_case_run_1.bugs.create(alias="test1")
        bug_2 = self.test_case_run_1.bugs.create(alias="test2")

        self.assertEqual(self.test_case_run_1.bugs.count(),
                         self.test_case_run_2.bugs_history.count())

        self.assertTrue(bug_1 in self.test_case_run_2.bugs_history.all())
        self.assertTrue(bug_2 in self.test_case_run_2.bugs_history.all())


    def test_bugs_history_overriding(self):
        bug_1 = self.test_case_run_1.bugs.create(alias="test1")
        bug_2 = self.test_case_run_1.bugs.create(alias="overriding_bug_1")
        bug_3 = self.test_case_run_1.bugs.create(alias="overriding_bug_2")

        self.test_case_run_2.bugs.create(alias="overriding_bug_1")
        self.test_case_run_2.bugs.create(alias="overriding_bug_2")

        self.assertEqual(self.test_case_run_2.bugs_history.count(), 1)
        self.assertTrue(bug_1 in self.test_case_run_2.bugs_history.all())
        self.assertTrue(bug_2 not in self.test_case_run_2.bugs_history.all())
        self.assertTrue(bug_3 not in self.test_case_run_2.bugs_history.all())


class TestCopyTestRun(TestCase):
    def setUp(self):
        self.test_case_directory = store.TestCaseDirectory.objects.create(parent=None,
                                                                          name="Root")
        self.test_case = store.TestCase.objects.create(name="test_case",
                                                       parent=self.test_case_directory)

        self.test_run_directory = models.TestRunDirectory.objects.create(parent=None,
                                                                          name="Root")

        self.test_run = models.TestRun.objects.create(name="test_run",
                                                      parent=self.test_run_directory)
        self.test_run.run(self.test_case)

    def test_copy(self):
        self.test_run_copy = self.test_run.copy()

        self.assertTrue(self.test_run_copy.name.startswith(self.test_run.name))
        self.assertTrue(self.test_run_copy.name.endswith("(copy)"))

        self.assertEqual([(element.origin.pk, element.name) for element in self.test_run.testcases.all()],
                         [(element.origin.pk, element.name) for element in self.test_run_copy.testcases.all()])
