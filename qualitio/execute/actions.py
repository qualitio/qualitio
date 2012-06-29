from django import forms
from django.conf import settings
from qualitio import actions, core, history
from qualitio.execute import models, forms as execute_forms


class ChangeParent(actions.ChangeParent):
    model = models.TestRun


class StatusForm(core.BaseForm):
    status = forms.ModelChoiceField(queryset=models.TestCaseRunStatus.objects.all(), required=True)


class TestCaseRunChangeStatus(actions.Action):
    label = "Change status"
    model = models.TestCaseRun
    form_class = StatusForm

    def run_action(self, data, queryset, form=None):
        queryset.update(status=form.cleaned_data['status'])
        return self.success(message=u'Status changed successfully.')


class TestCaseRunAddBug(actions.Action):
    label = "Add bug"
    model = models.TestCaseRun
    form_class = execute_forms.AddBugForm


    def get_issue_backend(self):
        from django.utils.importlib import import_module
        backend_name = getattr(settings, "ISSUE_BACKEND", None)
        issues_module = import_module(backend_name)
        return issues_module.Backend

    def download_bugs(self, bugs_ids):
        issues = self.get_issue_backend()
	try:
		zm = [issues.fetch_bug(bug_id) for bug_id in bugs_ids]
	except Exception as e:
                return "Issue server error meessage: ".join(e)
	return zm

    def format_error_msg(self, error):
        reason = u'; '.join(map(unicode, getattr(error, 'messages', [])))
        if not reason:
            reason = u'%s' % unicode(error)
        return reason

    def run_action(self, data, queryset, form):
        from django.db import transaction
	testcaserun = None
	downloaded_bugs = self.download_bugs(form.cleaned_data['bugs'])
	
	if isinstance(downloaded_bugs, basestring):
	   return self.failed(message=downloaded_bugs)
        try:
            with transaction.commit_on_success():
                bugs = []
                for testcaserun in queryset.all():
                    for downloaded_bug in downloaded_bugs:
                        bugs.append(testcaserun.bugs.get_or_create(**downloaded_bug)[0])
                log = history.History(self.request.user, testcaserun.parent)
                log.add_objects(created=bugs, prefix_object=testcaserun)
                log.save()
        except Exception, error:
            return self.failed(message='Adding bugs to "%s" failed: %s' % (
                    getattr(testcaserun, 'name', None),
                    self.format_error_msg(error)
                    ))
        return self.success(message='Bugs added!')


class RemoveBugForm(execute_forms.AddBugForm):
    pass


class TestCaseRunRemoveBug(actions.Action):
    label = "Remove bug"
    model = models.TestCaseRun
    form_class = RemoveBugForm

    def format_error_msg(self, error):
        reason = u'; '.join(map(unicode, getattr(error, 'messages', [])))
        if not reason:
            reason = u'%s' % unicode(error)
        return reason

    def run_action(self, data, queryset, form):
        from django.db import transaction
        aliases = form.cleaned_data['bugs']
        testcaserun = None

        try:
            with transaction.commit_on_success():
                bugs = []
                for testcaserun in queryset.all():
                    bugs = testcaserun.bugs.filter(alias__in=aliases)
                    deleted = list(bugs)
                    bugs.delete()

                    log = history.History(self.request.user, testcaserun.parent)
                    log.add_objects(deleted=deleted, prefix=True)
                    log.save()

        except Exception, error:
            return self.failed(message='Removing bugs from "%s" failed: %s' % (
                    getattr(testcaserun, 'name', None),
                    self.format_error_msg(error)
                    ))

        return self.success(message='Bugs removed!')
