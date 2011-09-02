from django.contrib.auth import models as auth
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (View, DetailView, CreateView, RedirectView,
                                  UpdateView, ListView, TemplateView, FormView)

from reversion.models import Revision
from articles.models import Article

from qualitio.core.utils import json_response, success, failed
from qualitio.execute.forms import TestRunStatusFormSet, TestCaseRunStatusFormSet

import models
import forms


class OrganizationObjectMixin(object):

    def get_object(self):
        slug = self.request.organization.name
        try:
            return models.Organization.objects.get(slug=slug)
        except models.Organization.DoesNotExist:
            raise Http404(u"No %(verbose_name)s found matching the query" %
                          {'verbose_name': models.Organization._meta.verbose_name})


class OrganizationDetails(View, OrganizationObjectMixin):
    def get(self, request, *args, **kwargs):
        if request.organization:
            return TemplateResponse(request, "projects/organization_detail.html",
                                    {"organization": request.organization})
        else:
            return TemplateResponse(request, "projects/organization_none.html")


class OrganizationSettings(TemplateView):
    template_name = "projects/organization_settings.html"

    class Profile(OrganizationObjectMixin, UpdateView):
        success_url = "/"
        form_class = forms.OrganizationProfileForm

    class Users(TemplateView):
        template_name = "projects/organization_settings_users_form.html"

        def get_context_data(self, **kwargs):
            context = super(OrganizationSettings.Users, self).get_context_data(**kwargs)
            context['formset'] = forms.OrganizationUsersForm()
            return context

        def get(self, request, *args, **kwargs):
            return self.render_to_response(self.get_context_data(**kwargs))

        @json_response
        def post(self, request, *args, **kwargs):
            formset = forms.OrganizationUsersForm(request.POST)
            if formset.is_valid():
                formset.save()
                return success(message='Changes saved.')

            return failed(message="Validation errors",
                          data=formset._errors_list())

    class Porjects(TemplateView):
        template_name = "projects/organization_settings_projects_form.html"

        def get_context_data(self, **kwargs):
            context = super(OrganizationSettings.Porjects, self).get_context_data(**kwargs)

            settings_form = []
            for project in models.Project.objects.all():
                settings_form.append({
                        'form': forms.ProjectForm(instance=project, prefix='general'),
                        'project': project,
                        'testcase_statuses': forms.ProjectTestCaseStatusFormSet(instance=project,
                                                                                prefix='store_testcase_status'),
                        'testrun_statuses': forms.ProjectTestRunStatusFormSet(instance=project,
                                                                              prefix='execute_testrun_status'),
                        'testcaserun_statuses': forms.ProjectTestCaseRunStatusFormSet(instance=project,
                                                                                      prefix='execute_testcaserun_status'),
                        'glossary_languages': forms.ProjectGlossaryLanguageFormSet(instance=project,
                                                                                   prefix='glossary_language')
                        })



            context['project_settings_forms'] = settings_form
            return context

        def get(self, request, *args, **kwargs):
            return self.render_to_response(self.get_context_data(**kwargs))

        @json_response
        def post(self, request, *args, **kwargs):
            project = models.Project.objects.get(pk=kwargs['pk'])
            form = forms.ProjectForm(request.POST,
                                     instance=project,
                                     prefix='general')

            store_testcase = forms.ProjectTestCaseStatusFormSet(request.POST,
                                                                instance=project,
                                                                prefix='store_testcase_status')

            execute_testrun = forms.ProjectTestRunStatusFormSet(request.POST,
                                                                instance=project,
                                                                prefix='execute_testrun_status')

            execute_testcaserun = forms.ProjectTestCaseRunStatusFormSet(request.POST,
                                                                        instance=project,
                                                                        prefix='execute_testcaserun_status')

            glossary_language = forms.ProjectGlossaryLanguageFormSet(request.POST,
                                                                     instance=project,
                                                                     prefix='glossary_language')


            if form.is_valid() and\
                    store_testcase.is_valid() and\
                    execute_testrun.is_valid() and\
                    execute_testcaserun.is_valid() and\
                    glossary_language.is_valid():

                form.save()
                store_testcase.save()
                execute_testrun.save()
                execute_testcaserun.save()
                glossary_language.save()
                return success(message='Changes saved.')

            return failed(message="Validation errors: %s" % form.error_message(),
                          data=store_testcase._errors_list() +\
                              execute_testrun._errors_list() +\
                              execute_testcaserun._errors_list() +\
                              glossary_language._errors_list())


class ProjectList(ListView):
    model = models.Project
    context_object_name = "project_list"

    def get_context_data(self, **kwargs):
        context = super(ProjectList, self).get_context_data(**kwargs)
        context['revisons'] =\
            Revision.objects.filter(user=self.request.user).order_by("-date_created")
        context['articles'] = Article.objects.filter(status__name="Finished")
        return context

    def get_queryset(self):
        return self.model._default_manager.all()


class ProjectDetails(RedirectView):
    def get_redirect_url(self, **kwargs):
        return "%srequire/" % self.request.project.get_absolute_url()


class ProjectNew(CreateView):
    model = models.Project
    form_class = forms.ProjectForm

    @json_response
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.organization = self.request.organization
        self.object.save()
        self.object.setup()

        return success(message='project created',
                       data={"url": self.object.get_absolute_url() })

    @json_response
    def form_invalid(self, form):
        return failed(message="Validation errors: %s" % form.error_message(),
                      data=form.errors_list())
