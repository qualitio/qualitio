from django.http import Http404
from django.core.urlresolvers import reverse
from django.core.mail import send_mail, mail_managers
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import redirect, render_to_response
from django.contrib.auth import logout
from django.contrib.auth import models as auth
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (View, CreateView, RedirectView,
                                  UpdateView, ListView, TemplateView,
                                  FormView)

from reversion.models import Revision
from articles.models import Article

from qualitio.core.utils import json_response, success, failed
from qualitio.organizations import models
from qualitio.organizations import forms


class OrganizationObjectMixin(object):

    def get_object(self):
        slug = self.request.organization.slug
        try:
            return models.Organization.objects.get(slug=slug)
        except models.Organization.DoesNotExist:
            raise Http404(u"No %(verbose_name)s found matching the query" %
                          {'verbose_name': models.Organization._meta.verbose_name})


class OrganizationDetails(View, OrganizationObjectMixin):
    def get(self, request, *args, **kwargs):
        if request.organization:
            articles = Article.objects.filter(status__name="Finished")
            return TemplateResponse(request, "organizations/organization_detail.html",
                                    {"organization": request.organization,
                                     "articles": articles})
        else:
            return redirect("organization_none")


class OrganizationNone(TemplateView):
    template_name = "organizations/organization_none.html"

    def get(self, *kwargs):
        organization_form = forms.OrganizationNew()
        
        return self.render_to_response({
            "organization_form": organization_form,
        })

    def post(self, *kwargs):
        organization_form = forms.OrganizationNew(self.request.POST)

        if organization_form.is_valid():

            emails = filter(len, auth.User.objects.filter(is_superuser=True).values_list(
                'email', flat=True))

            send_mail(
                'Qualitio Project, New organization request',
                render_to_string('organizations/organization_request.mail',{
                    'email': organization_form.cleaned_data['email'],
                    'organization_name': organization_form.cleaned_data['name'],
                }),
                'Qualitio Notifications <notifications@qualitio.com>',
                emails)
            
            return redirect("organization_request_thanks")
        
        return self.render_to_response({
            "organization_form": organization_form,
        })


class OrganizationRequestThanks(TemplateView):
    template_name = "organizations/organization_request_thanks.html"
    

class UserInactive(TemplateView):
    template_name = "organizations/user_inactive.html"

    def get(self, *args, **kwargs):
        logout(self.request)
        return super(UserInactive, self).get(*args, **kwargs)

class OrganizationSettings(RedirectView):
    url = '/settings/profile/'

    class Profile(OrganizationObjectMixin, UpdateView):
        form_class = forms.OrganizationProfileForm

        @json_response
        def form_valid(self, form):
            self.object = form.save()
            return success(message="Organization profile successfully updated.")

        @json_response
        def form_invalid(self, form):
            return failed(message=form.error_message(),
                          data=form.errors_list())

    class Members(TemplateView):
        template_name = "organizations/organization_settings_members.html"

    class MembersList(TemplateView):
        template_name = "organizations/organization_settings_members_list.html"

        def get(self, request):
            return self.render_to_response({
                'active_users_count': self.request.organization.organizationmember_set.exclude(
                    role=models.OrganizationMember.INACTIVE
                ).count(),
                'formset': forms.OrganizationUsersForm(
                    instance=self.request.organization
                )
            })

        @json_response
        def post(self, request):
            formset = forms.OrganizationUsersForm(
                request.POST,
                instance=self.request.organization
            )

            if formset.is_valid():
                formset.save()
                return success(message='Changes saved.')

            return failed(message="%s"
                          % formset.non_form_errors().as_text())


    class MemberNew(OrganizationObjectMixin, TemplateView):
        template_name = "organizations/organization_settings_members_new.html"

        get_context_data = lambda self: {
            'member_form': forms.NewMemberForm(prefix="member_form"),
            'user_form': forms.NewUserForm(prefix="user_form")
        }

        @json_response # ToDo: maybe split this into two separte views.
        def post(self, request):
            if request.REQUEST.has_key('new_user'):
                form = forms.NewUserForm(request.POST, prefix="user_form")
                if form.is_valid():
                    user = form.save(commit=False)
                    user.username = form.cleaned_data["email"]
                    user.set_password(form.cleaned_data["password1"])
                    user.save()
                    
                    models.OrganizationMember.objects.create(
                        user=user,
                        organization=request.organization,
                        role=models.OrganizationMember.INACTIVE
                    )

                    send_mail(
                        'Qualitio Project, User account created in %s organization'
                        % self.request.organization.name,
                        render_to_string('organizations/new_user.mail',
                                         {"organization": self.request.organization,
                                          "user": user,
                                          "password": form.cleaned_data["password1"]}),
                        'Qualitio Notifications <notifications@qualitio.com>',
                        [user.email])
                    
                    return success(message="User created.")

            else:
                form = forms.NewMemberForm(request.POST, prefix="member_form")
                if form.is_valid():
                    email = form.cleaned_data.get('email')
                    try:
                        user = auth.User.objects.get(email=email)

                        send_mail(
                            'Qualitio Project, Invitation to %s organization'
                            % self.request.organization.name,
                            render_to_string('organizations/new_member.mail',
                                             {"organization": self.request.organization,
                                              "user": user}),
                            'Qualitio Notifications <notifications@qualitio.com>',
                            [email])
                        
                        models.OrganizationMember.objects.create(
                            user=user,
                            organization=request.organization,
                            role=models.OrganizationMember.INACTIVE
                        )
                        return success(message="User added!", data={'created': True})
                    except auth.User.DoesNotExist:
                        return success(message="Does not exist, you need to create account!",
                                       data={'created': False,
                                             'email': email})

            return failed(message="Validation errors", data=form.errors_list())


    class Projects(TemplateView):
        template_name = "organizations/organization_settings_projects_form.html"

        def get_context_data(self, **kwargs):
            context = super(OrganizationSettings.Projects, self).get_context_data(**kwargs)

            settings_form = []
            for project in models.Project.objects.all():
                settings_form.append({
                        'form': forms.ProjectForm(instance=project, prefix='general', organization=self.request.organization),
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
                                     prefix='general',
                                     organization=request.organization)

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
                          data=form.errors_list() +\
                              store_testcase._errors_list() +\
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

    def get_form_kwargs(self):
        kwargs = super(ProjectNew, self).get_form_kwargs()
        kwargs.update(organization=self.request.organization)
        return kwargs

    @json_response
    def form_valid(self, form):
        self.object = form.save()
        self.object.setup()
        return success(message='project created',
                       data={"url": self.object.get_absolute_url() })

    @json_response
    def form_invalid(self, form):
        return failed(message="Validation errors: %s" % form.error_message(),
                      data=form.errors_list())




class GoogleAppsRedirect(RedirectView):

    permanent = False

    def _get_url(self, organization):
        if self.request.is_secure():
            return "https://%s.%s" % (organization.slug, self.request.get_host())
        return "http://%s.%s" % (organization.slug, self.request.get_host())

    def get_redirect_url(self, **kwargs):
        try:
            googleapps_domain = self.kwargs['domain']
            organization = models.Organization.objects.get(
                googleapps_domain=googleapps_domain
            )
            return self._get_url(organization)

        except (KeyError, models.Organization.DoesNotExist):
            raise Http404


class GoogleAppsSetupRedirect(GoogleAppsRedirect):

    def get_redirect_url(self, **kwargs):
        try:
            organization = models.Organization.objects.get(
                googleapps_domain=self.kwargs['domain']
            )

            return "%s/settings/" % self._get_url(organization)

        except models.Organization.DoesNotExist:
            organization = models.Organization.objects.create(
                googleapps_domain=self.kwargs['domain'],
                name=self.kwargs['domain']
            )
            return "%s/googleapps_setup/?%s" % (self._get_url(organization),
                                                self.request.META['QUERY_STRING'])


def googleapps_domain_setup(request, *args, **kwargs):

    if not request.user.is_authenticated():
        return redirect("%s?next=%s" % (reverse("socialauth_begin", args=['googleapps']),
                                        request.get_full_path()))

    if request.method == "GET":
        form = forms.OrganizationGoogleAppsSetupForm(instance=request.organization)
        form.fields['callback'].initial = request.GET.get('callback')
    else:

        form = forms.OrganizationGoogleAppsSetupForm(request.POST,
                                                     instance=request.organization)

        if form.is_valid():
            organization = form.save()
            models.OrganizationMember.objects.create(
                user=request.user,
                organization=organization,
                role=models.OrganizationMember.INACTIVE
            )
            if request.POST.get('callback'):
                return redirect(request.POST.get('callback'))

    return render_to_response("organizations/organization_googleapps_setup.html",
                              {"form": form},
                              context_instance=RequestContext(request))


from django.views.decorators.csrf import csrf_exempt, csrf_protect

@csrf_exempt
def google_checkout(request, *args, **kwargs):
    from django.http import HttpResponse
    with open("/tmp/google_checkout", "w") as f:
        for name, value in request.POST.items():
            f.write("%s   %s\n" % (name, value))

    f.write("\n=================\n")
    return HttpResponse("")
