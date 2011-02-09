from nose.tools import *

from qualitio import store

import models



def test_run_test_case():
    test_case = store.TestCase.objects.create(name="name",
                                              precondition="precondtion",
                                              description="description")

    test_case_run = models.TestCaseRun.run(test_case)

    assert_equals(test_case.name, test_case_run.name)
    assert_equals(test_case.description, test_case_run.description)
    assert_equals(test_case.precondition, test_case_run.precondition)

    assert_equals(test_case.steps.count(),
                  test_case_run.steps.count())


def test_run_test_case_with_steps():
    test_case = store.TestCase.objects.create(name="test_name",
                                              precondition="test_precondtion",
                                              description="test_description")

    test_case.steps.create(description="step_1_description",
                           expected="step_1_excpected",
                           sequence=0)

    test_case.steps.create(description="step_2_description",
                           expected="step_2_excpected",
                           sequence=1)

    test_case_run = models.TestCaseRun.run(test_case)

    assert_equals(test_case.steps.count(),
                  test_case_run.steps.count())

    for test_case_step in test_case.steps.all():
        test_case_run_step = test_case_run.steps.get(sequence=test_case_step.sequence)
        assert_equals(test_case_step.description, test_case_run_step.description)
        assert_equals(test_case_step.expected, test_case_run_step.expected)
