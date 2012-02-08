from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization

from qualitio import require
from qualitio import store
from qualitio import execute
from qualitio import glossary

from qualitio import THREAD

# customized tastypie classes
from qualitio.core.custommodel import ModelResource, Api

api = Api(api_name="api")

# Monkey path, we don't really need xml and yaml.
Serializer.formats = ['json']
Serializer.content_types = {'json': 'application/json'}


class BaseProjectResource(ModelResource):
    def get_resource_uri(self, bundle_or_obj):
        resource_uri = super(BaseProjectResource, self).get_resource_uri(bundle_or_obj)
        return resource_uri.replace('/x/', '/%s/' % bundle_or_obj.obj.project.slug)

    def get_object_list(self, request):
        qs = super(ModelResource, self).get_object_list(request)
        if qs and request:
            return qs.filter(project=request.project)
        return qs

class BaseMeta(object):
    default_format = 'application/json'
    serializer = Serializer(formats=Serializer.formats, content_types=Serializer.content_types)
    authentication = BasicAuthentication()
    authorization = DjangoAuthorization()

class DirectoryMeta(BaseMeta):
    excludes = ['tree_id', 'rght', 'lft', 'level', 'is_superuser']
    filtering = {'parent': ALL_WITH_RELATIONS,
                 'path': ALL,
                 'name': ALL}


class StateMeta(BaseMeta):
    excludes = ['created_time', 'modified_time']
    filtering = {'name': ALL}


class RequirementResource(BaseProjectResource):
    parent = fields.ForeignKey('self', 'parent', null=True)

    class Meta(DirectoryMeta):
        queryset = require.Requirement.objects.all()
        resource_name = 'require/requirement'
api.register(RequirementResource())


class TestCaseDirectoryResource(BaseProjectResource):
    parent = fields.ToOneField('self', 'parent', null=True)

    class Meta(DirectoryMeta):
        queryset = store.TestCaseDirectory.objects.all()
        resource_name = 'store/testcasedirectory'
api.register(TestCaseDirectoryResource())


class TestCaseStatusResource(BaseProjectResource):
    class Meta(StateMeta):
        queryset = store.TestCaseStatus.objects.all()
        resource_name = 'store/testcasestatus'
api.register(TestCaseStatusResource())


class TestCaseStepResource(BaseProjectResource):
    testcase = fields.ToOneField('api.TestCaseResource', 'testcase')

    class Meta(BaseMeta):
        queryset = store.TestCaseStep.objects.all()
        resource_name = 'store/testcasestep'
api.register(TestCaseStepResource())


class TestCaseResource(BaseProjectResource):
    parent = fields.ForeignKey(TestCaseDirectoryResource, 'parent')
    status = fields.ForeignKey(TestCaseStatusResource, 'status', full=True)
    steps = fields.ToManyField(TestCaseStepResource, 'steps', full=True)

    class Meta(BaseMeta):
        queryset = store.TestCase.objects.all()
        resource_name = 'store/testcase'
        filtering = {'parent': ALL_WITH_RELATIONS,
                     'status': ALL_WITH_RELATIONS,
                     'steps': ALL_WITH_RELATIONS,
                     'description': ALL,
                     'precondition': ALL,
                     'path': ALL,
                     'name': ALL}
api.register(TestCaseResource())


class TestRunDirectoryResource(BaseProjectResource):
    parent = fields.ToOneField('self', 'parent', null=True)

    class Meta(DirectoryMeta):
        queryset = execute.TestRunDirectory.objects.all()
        resource_name = 'execute/testrundirectory'
api.register(TestRunDirectoryResource())


class TestRunStatusResource(BaseProjectResource):
    class Meta(StateMeta):
        queryset = execute.TestRunStatus.objects.all()
        resource_name = 'execute/testrunstatus'
api.register(TestRunStatusResource())


class TestCaseStepRunResource(BaseProjectResource):
    class Meta(BaseMeta):
        queryset = execute.TestCaseRun.objects.all()
        resource_name = 'execute/testcasesteprun'
api.register(TestCaseStepRunResource())


class BugResource(BaseProjectResource):
    class Meta(BaseMeta):
        queryset = execute.Bug.objects.all()
        resource_name = 'execute/bug'
api.register(BugResource())


class TestCaseRunResource(BaseProjectResource):
    steps = fields.ToManyField(TestCaseStepResource, 'steps', full=True)
    bugs = fields.ToManyField(BugResource, 'steps', full=True)

    class Meta(BaseMeta):
        queryset = execute.TestCaseRun.objects.all()
        resource_name = 'execute/testcaserun'
api.register(TestCaseRunResource())


class TestRunResource(BaseProjectResource):
    status = fields.ForeignKey(TestRunStatusResource, 'status', full=True)
    testcases = fields.ToManyField(TestCaseStepResource, 'testcases', full=True)
    class Meta(DirectoryMeta):
        queryset = execute.TestRun.objects.all()
        resource_name = 'execute/testrun'
api.register(TestRunResource())


class LanguageResource(BaseProjectResource):
    class Meta(StateMeta):
        queryset = glossary.Language.objects.all()
        resource_name = 'glossary/language'
api.register(LanguageResource())


class RepresentationResource(BaseProjectResource):
    language = fields.ForeignKey(TestRunStatusResource, 'language', full=True)
    class Meta(DirectoryMeta):
        queryset = glossary.Representation.objects.all()
        resource_name = 'glossary/representation'
api.register(RepresentationResource())


class WordResource(BaseProjectResource):
    representations = fields.ToManyField(RepresentationResource, 'representation_set', full=True)
    class Meta(DirectoryMeta):
        queryset = glossary.Word.objects.all()
        resource_name = 'glossary/word'
api.register(WordResource())


urls = api.urls
