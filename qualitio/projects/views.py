from django.views.generic import DetailView, TemplateView, CreateView, UpdateView, ListView
from qualitio.core.utils import json_response, success, failed

from reversion.models import Revision
from articles.models import Article

from models import Project
from forms import ProjectForm


class Index(TemplateView):
    template_name = 'secret.html'


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

