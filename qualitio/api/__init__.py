from tastypie.resources import ModelResource
from tastypie.api import Api
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization

api = Api(api_name="api")

from qualitio import require
from qualitio import store
from qualitio import execute
from qualitio import glossary

# Monkey path, we don't really need xml and yaml.
Serializer.formats = ['json']
Serializer.content_types = {'json': 'application/json'}


class BaseMeta(object):
    default_format = 'application/json'
    serializer = Serializer(formats=Serializer.formats, content_types=Serializer.content_types)
    authentication = BasicAuthentication()
    authorization = DjangoAuthorization()


class DirectoryMeta(BaseMeta):
    excludes = ['tree_id', 'rght', 'lft', 'level', 'is_superuser']


class StateMeta(BaseMeta):
    excludes = ['created_time', 'modified_time']


class RequirementResource(ModelResource):
    parent = fields.ForeignKey('self', 'parent', null=True)
    class Meta(DirectoryMeta):
        queryset = require.Requirement.objects.all()
        resource_name = 'require/requirement'
api.register(RequirementResource())


class TestCaseDirectoryResource(ModelResource):
    class Meta(DirectoryMeta):
        queryset = store.TestCaseDirectory.objects.all()
        resource_name = 'store/testcasedirectory'
api.register(TestCaseDirectoryResource())


class TestCaseStatusResource(ModelResource):
    class Meta(StateMeta):
        queryset = store.TestCaseStatus.objects.all()
        resource_name = 'store/testcasestatus'
api.register(TestCaseStatusResource())


class TestCaseStepResource(ModelResource):
    class Meta(BaseMeta):
        queryset = store.TestCaseStep.objects.all()
        resource_name = 'store/testcasestep'
api.register(TestCaseStepResource())


class TestCaseResource(ModelResource):
    parent = fields.ForeignKey(TestCaseDirectoryResource, 'parent')
    status = fields.ForeignKey(TestCaseStatusResource, 'status', full=True)
    steps = fields.ToManyField(TestCaseStepResource, 'steps', full=True)

    class Meta(BaseMeta):
        queryset = store.TestCase.objects.all()
        resource_name = 'store/testcase'
api.register(TestCaseResource())


class TestRunDirectoryResource(ModelResource):
    class Meta(DirectoryMeta):
        queryset = execute.TestRunDirectory.objects.all()
        resource_name = 'execute/testrundirectory'
api.register(TestRunDirectoryResource())


class TestRunStatusResource(ModelResource):
    class Meta(StateMeta):
        queryset = execute.TestRunStatus.objects.all()
        resource_name = 'execute/testrunstatus'
api.register(TestRunStatusResource())


class TestCaseStepRunResource(ModelResource):
    class Meta(BaseMeta):
        queryset = execute.TestCaseRun.objects.all()
        resource_name = 'execute/testcasesteprun'
api.register(TestCaseStepRunResource())


class BugResource(ModelResource):
    class Meta(BaseMeta):
        queryset = execute.Bug.objects.all()
        resource_name = 'execute/bug'
api.register(BugResource())


class TestCaseRunResource(ModelResource):
    steps = fields.ToManyField(TestCaseStepResource, 'steps', full=True)
    bugs = fields.ToManyField(BugResource, 'steps', full=True)

    class Meta(BaseMeta):
        queryset = execute.TestCaseRun.objects.all()
        resource_name = 'execute/testcaserun'
api.register(TestCaseRunResource())


class TestRunResource(ModelResource):
    status = fields.ForeignKey(TestRunStatusResource, 'status', full=True)
    testcases = fields.ToManyField(TestCaseStepResource, 'testcases', full=True)
    class Meta(DirectoryMeta):
        queryset = execute.TestRun.objects.all()
        resource_name = 'execute/testrun'
api.register(TestRunResource())


class LanguageResource(ModelResource):
    class Meta(StateMeta):
        queryset = glossary.Language.objects.all()
        resource_name = 'glossary/language'
api.register(LanguageResource())


class RepresentationResource(ModelResource):
    language = fields.ForeignKey(TestRunStatusResource, 'language', full=True)
    class Meta(DirectoryMeta):
        queryset = glossary.Representation.objects.all()
        resource_name = 'glossary/representation'
api.register(RepresentationResource())


class WordResource(ModelResource):
    representations = fields.ToManyField(RepresentationResource, 'representation_set', full=True)
    class Meta(DirectoryMeta):
        queryset = glossary.Word.objects.all()
        resource_name = 'glossary/word'
api.register(WordResource())


urls = api.urls
