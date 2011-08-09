from django.views.generic import DetailView, TemplateView, CreateView, UpdateView, ListView # , ProcessFormView
from django.db.models import get_model

from reversion.models import Revision
from articles.models import Article

from qualitio.core.utils import json_response, success, failed
from qualitio import store
from qualitio.projects.models import Project
from qualitio.projects.forms import ProjectForm
from qualitio.store.forms import TestCaseStatusFormSet
from qualitio.execute.forms import TestRunStatusFormSet, TestCaseRunStatusFormSet


class ProjectList(ListView):
    model = Project
    context_object_name = "project_list"

    def get_context_data(self, **kwargs):
        context = super(ProjectList, self).get_context_data(**kwargs)
        context['revisons'] =\
            Revision.objects.filter(user=self.request.user).order_by("-date_created")
        context['articles'] = Article.objects.filter(status__name="Finished")
        return context


class ProjectDetails(DetailView):
    model = Project


class ProjectSettingsEdit(TemplateView):
    template_name = 'projects/settings_form.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectSettingsEdit, self).get_context_data(**kwargs)
        context['testcase_status_formset'] = TestCaseStatusFormSet(prefix="testcase")
        context['testrun_status_formset'] = TestRunStatusFormSet(prefix="testrun")
        context['testcaserun_status_formset'] = TestCaseRunStatusFormSet(prefix="testcaserun")
        context['project'] = Project.objects.get(slug=kwargs['slug'])
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    @json_response
    def post(self, request, *args, **kwargs):
        formsets = [TestCaseStatusFormSet(request.POST, prefix="testcase"),
                    TestRunStatusFormSet(request.POST, prefix="testrun"),
                    TestCaseRunStatusFormSet(request.POST, prefix="testcaserun")]

        if all([formset.is_valid for formset in formsets]):
            all([formset.save() for formset in formsets])
            return success(message='Test case statuses updated')

        return failed(message="Validation errors: %s",
                      data=all([formset._errors_list() for formset in formsets]))


class ProjectNew(CreateView):
    model = Project
    form_class = ProjectForm

    @json_response
    def form_valid(self, form):
        self.object = form.save()

        #ToDo: maybe move it to project.save
        from qualitio.require import Requirement
        from qualitio.store import TestCaseDirectory
        from qualitio.execute import TestRunDirectory
        from qualitio.report import ReportDirectory

        Requirement.objects.create(name=self.object.name, project=self.object)
        TestCaseDirectory.objects.create(name=self.object.name, project=self.object)
        TestRunDirectory.objects.create(name=self.object.name, project=self.object)
        ReportDirectory.objects.create(name=self.object.name, project=self.object)

        return success(message='project created',
                       data={"url": self.object.get_absolute_url() })

    @json_response
    def form_invalid(self, form):
        return failed(message="Validation errors: %s" % form.error_message(),
                      data=form.errors_list())


class ProjectEdit(UpdateView):
    model = Project
    form_class = ProjectForm

    @json_response
    def form_valid(self, form):
        self.object = form.save()
        return success(message='project updated',
                       data={"object_id": self.object.pk})

    @json_response
    def form_invalid(self, form):
        return failed(message="Validation errors: %s" % form.error_message(),
                      data=form.errors_list())

