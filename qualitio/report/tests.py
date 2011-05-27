from django.test import TestCase
from django.db.models.query import QuerySet

from qualitio import store
from qualitio.report.models import ReportDirectory, Report, ContextElement
from django.core.exceptions import ValidationError


class TestContextElementValidation(TestCase):
    def setUp(self):
        self.root = ReportDirectory.objects.create(name="root")
        self.report = Report.objects.create(name="report", parent=self.root)


    def test_invalid_object(self):
        query = "XyX.all()"

        context_element = ContextElement.objects.create(report=self.report,
                                                        name="context_element",
                                                        query=query)

        self.assertRaises(ValidationError, context_element.full_clean)


    def test_invalid_short_query(self):
        query = "TestCase"

        context_element = ContextElement.objects.create(report=self.report,
                                                        name="context_element",
                                                        query=query)

        self.assertRaises(ValidationError, context_element.full_clean)

    def test_invalid_method(self):
        query = "TestCase.delete()"

        context_element = ContextElement.objects.create(report=self.report,
                                                        name="context_element",
                                                        query=query)

        self.assertRaises(ValidationError, context_element.full_clean)


class TestContextElementQueryBuild(TestCase):
    def setUp(self):
        self.root = ReportDirectory.objects.create(name="root")
        self.report = Report.objects.create(name="report", parent=self.root)


    def test_build(self):
        root = store.TestCaseDirectory.objects.create(name="root")
        testcase = store.TestCase.objects.create(name="test",
                                                 parent=root)

        object_name = "TestCase"
        methods = [("all", {})]

        query = ContextElement._build_query(object_name, methods)

        self.assertTrue(isinstance(query, QuerySet))
        self.assertTrue(testcase in query)


    def test_build_exclude(self):
        root = store.TestCaseDirectory.objects.create(name="root")
        testcase1 = store.TestCase.objects.create(name="test1",
                                                 parent=root)

        testcase2 = store.TestCase.objects.create(name="test2",
                                                  parent=root)

        object_name = "TestCase"
        methods = [("all", {}), ("exclude", {"pk": testcase1.pk})]

        query = ContextElement._build_query(object_name, methods)

        self.assertTrue(isinstance(query, QuerySet))
        self.assertTrue(testcase2 in query)


    def test_build_get(self):
        root = store.TestCaseDirectory.objects.create(name="root")
        testcase = store.TestCase.objects.create(name="test1",
                                                 parent=root)

        object_name = "TestCase"
        methods = [("get", {"pk": testcase.pk})]

        query = ContextElement._build_query(object_name, methods)

        self.assertEquals(query, testcase)

    def test_build_get_empty(self):
        object_name = "TestCase"
        methods = [ ("get", {"pk": 1} )]

        query = ContextElement._build_query(object_name, methods)

        self.assertEquals(query, None)


class TestContextElementQuerySet(TestCase):
    def setUp(self):
        self.report_root = ReportDirectory.objects.create(name="root")
        self.report = Report.objects.create(name="report", parent=self.report_root)

        self.testcase_root = store.TestCaseDirectory.objects.create(name="root")
        self.testcase1 = store.TestCase.objects.create(name="testcase1",
                                                       parent=self.testcase_root)

        self.testcase2 = store.TestCase.objects.create(name="testcase2",
                                                       parent=self.testcase_root)

        self.testcase3 = store.TestCase.objects.create(name="testcase3",
                                                       parent=self.testcase_root)

    def test_queryset_all(self):
        query = "TestCase.all()"

        context_element = ContextElement.objects.create(report=self.report,
                                                        name="context_element",
                                                        query=query)
        context_element.full_clean()
        queryset = context_element.query_object()

        self.assertTrue(self.testcase1 in queryset)
        self.assertTrue(self.testcase2 in queryset)
        self.assertTrue(self.testcase3 in queryset)


    def test_queryset_filter(self):
        query = "TestCase.filter(pk=1)"

        context_element = ContextElement.objects.create(report=self.report,
                                                        name="context_element",
                                                        query=query)

        context_element.full_clean()
        queryset = context_element.query_object()

        self.assertTrue(self.testcase1 in queryset)
        self.assertTrue(self.testcase2 not in queryset)
        self.assertTrue(self.testcase3 not in queryset)


    def test_queryset_get(self):
        query = "TestCase.get(pk=1)"

        context_element = ContextElement.objects.create(report=self.report,
                                                        name="context_element",
                                                        query=query)

        context_element.full_clean()
        queryset = context_element.query_object()

        self.assertTrue(queryset,self.testcase1)


    def test_queryset_exclude(self):
        query = "TestCase.exclude(pk=1)"

        context_element = ContextElement.objects.create(report=self.report,
                                                        name="context_element",
                                                        query=query)

        context_element.full_clean()
        queryset = context_element.query_object()

        self.assertTrue(self.testcase1 not in queryset)
        self.assertTrue(self.testcase2 in queryset)
        self.assertTrue(self.testcase3 in queryset)

        self.assertTrue(queryset,self.testcase1)

    def test_queryset_combine(self):
        testcase4 = store.TestCase.objects.create(name="Testcase4",
                                                  parent=self.testcase_root)

        query = 'TestCase.exclude(pk=1).filter(name__startswith="Test")'

        context_element = ContextElement.objects.create(report=self.report,
                                                        name="context_element",
                                                        query=query)

        context_element.full_clean()
        queryset = context_element.query_object()

        self.assertTrue(testcase4 in queryset)


    def test_queryset_invalid(self):
        store.TestCase.objects.create(name="Testcase4",
                                      parent=self.testcase_root)

        query = 'TestCase.filter(name__sssstartswith="Test")'

        context_element = ContextElement.objects.create(report=self.report,
                                                        name="context_element",
                                                        query=query)

        self.assertRaises(ValidationError, context_element.full_clean)

