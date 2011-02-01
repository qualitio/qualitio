from django import forms
from django.core.exceptions import ValidationError

from qualitio.requirements.models import Requirement


class BaseRequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement

    def _post_clean(self):
        # '_post_clean' hook is responsible for model validation on ModelForm.
        # We need addintional validation of dependencies.
        super(BaseRequirementForm, self)._post_clean()

        # If 'dependencies' already have errors we shouldn't check it
        if not 'dependencies' in self._errors:
            try:
                self.instance.clean_dependencies(self.cleaned_data['dependencies'])
            except ValidationError, e:
                self._update_errors(e.message_dict)

    def save(self, clean_dependencies=False, *args, **kwargs):
        # The default behaviour of RequirementForm.save cannot invoke
        # additional check for dependencies cycles on model because it's
        # already done in '_post_clean' method.

        # Because of the implementation of 'save' procedure in
        # django.forms.models module, we need to change the 'save' method
        # behaviour on self.instance just for the moment when this ModelForm
        # instance will invoke it.
        # TODO: maybe we should discuss this if Proxy for self.instance with
        #       overriden 'save' method fits better here.

        original_save = None

        if not clean_dependencies and self.instance:
            def save(*a, **k):
                original_save(clean_dependencies=False, *a, **k)
            original_save = self.instance.save
            self.instance.save = save

        self.instance = super(BaseRequirementForm, self).save(*args, **kwargs)

        # If 'save' method was changed make sure to restore the changes
        if original_save:
            self.instance.save = original_save

        return self.instance


class RequirementForm(BaseRequirementForm):
    def __init__(self, *args, **kwargs):
        super(RequirementForm, self).__init__(*args, **kwargs)
        if self.instance:
            qs = Requirement.objects.exclude_potential_cycles(self.instance)
            self.fields['dependencies'].queryset = qs
        self.fields['dependencies'].required = False

    class Meta:
        model = Requirement
        fields = ("parent", "name", "release_target", "description", "dependencies")
        widgets = {"release_target": forms.DateInput(attrs={"class": "date-field"})}


class SearchTestcasesForm(forms.Form):
    search = forms.CharField(required=True, min_length=3)
