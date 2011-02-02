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


class PathModelForm(BaseModelForm):
    class Meta:
        exclude = ("path",)
