from django.views.generic import (View, DetailView, CreateView,
                                  UpdateView, ListView, TemplateView, FormView)

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import models as auth

from reversion.models import Revision
from articles.models import Article

from qualitio.core.utils import json_response, success, failed
from qualitio.execute.forms import TestRunStatusFormSet, TestCaseRunStatusFormSet
from qualitio.projects.forms import ProjectForm, ProjectUserForm
from qualitio.projects.models import Project
from qualitio.store.forms import TestCaseStatusFormSet


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


class ProjectNew(CreateView):
    model = Project
    form_class = ProjectForm

    @json_response
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        self.object.setup()

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


class ProjectUsersEdit(FormView):
    template_name = 'projects/users_form.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectUsersEdit, self).get_context_data(**kwargs)
        context['form'] = ProjectUserForm()
        context['project'] = Project.objects.get(slug=kwargs['slug'])
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    @json_response
    def post(self, request, *args, **kwargs):

        form = ProjectUserForm(request.POST)
        if form.is_valid():
            user = auth.User.objects.get(username=form.cleaned_data['username'])

            project = Project.objects.get(slug=kwargs['slug'])
            project.team.add(user)
            return success(message='User added to project')

        return failed(message="Validation errors: %s" % form.error_message(),
                      data=form.errors_list())


class ProjectUserRemove(View):

    @json_response
    def post(self, request, *args, **kwargs):
        user = auth.User.objects.get(username=kwargs['username'])
        project = Project.objects.get(slug=kwargs['slug'])
        project.team.remove(user)
        return success(message='User removed')


    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ProjectUserRemove, self).dispatch(*args, **kwargs)
