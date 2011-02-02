# Has to be applied to DirectoryModelForms
from mptt.forms import MoveNodeForm

from django import forms


class FormErrorProcessingMixin(object):
    def errors_list(self):
        """
        Returns all errors as list of tuples: (field_name, first_of_field_errors)
        """
        return [(fname, errors[0]) for fname, errors in self.errors.items()]

    def error_message(self):
        """
        Creates short, user readable message about what is wrong with the form.
        The message is created from a list of non_field_errors.
        """
        return ' '.join([e for e in self.non_field_errors()])


class BaseForm(forms.Form, FormErrorProcessingMixin):
    pass


class BaseModelForm(forms.ModelForm, FormErrorProcessingMixin):
    pass


class BaseInlineFormSet(forms.models.BaseInlineFormSet):
    """
    BaseInlineFormSet with additional error processing functionality.
    """
    def errors_list(self):
        formset_errors = []
        for i, error in filter(lambda x: x[1], list(enumerate(self.errors))):
            for v, k in error.items():
                formset_errors.append(map(lambda x: (("testcasestep_set-%s-%s") % (i, v), x), k)[0])
        return formset_errors



class PathModelForm(BaseModelForm):
    class Meta:
        exclude = ("path",)
