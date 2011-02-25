from django import forms
from django.core.exceptions import ValidationError

from qualitio import core
from qualitio.requirements.models import Requirement


class RequirementForm(core.DirectoryModelForm):

    class Meta(core.DirectoryModelForm.Meta):
        model = Requirement
        widgets = {"release_target": forms.DateInput(attrs={"class": "date-field"})}

    def __init__(self, *args, **kwargs):
        super(RequirementForm, self).__init__(*args, **kwargs)
        if self.instance:
            qs = Requirement.objects.exclude_potential_cycles(self.instance)
            self.fields['dependencies'].queryset = qs
        self.fields['dependencies'].required = False

    # TODO: do we really need it?
    def _post_clean(self):
        # '_post_clean' hook is responsible for model validation on ModelForm.
        # We need addintional validation of dependencies.
        super(RequirementForm, self)._post_clean()

        # If 'dependencies' already have errors we shouldn't check it
        if not 'dependencies' in self._errors:
            try:
                self.instance.clean_dependencies(self.cleaned_data['dependencies'])
            except ValidationError, e:
                self._update_errors(e.message_dict)

    def save(self, clean_dependencies=False, *args, **kwargs):
        kwargs['model_save_kwargs'] = {'clean_dependencies': clean_dependencies}
        return super(RequirementForm, self).save(*args, **kwargs)



class SearchTestcasesForm(core.BaseForm):
    search = forms.CharField(required=True, min_length=3)
