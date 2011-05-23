from qualitio.execute import models
from qualitio.filter import actions


# class TestCaseRunStatusChooseForm(actions.ActionForm):
#     status = forms.ModelChoiceField(queryset=models.TestCaseRunStatus.objects.all())


# class ChangeStatusAction(actions.Action):
#     name = 'setrequirement'
#     label = 'Set requirement action'
#     model = models.TestRun
#     form_class = TestCaseRunStatusChooseForm

#     def run_action(self, data, queryset, form=None):
#         queryset.update(requirement=form.cleaned_data.get('requirement'))
