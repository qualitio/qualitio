# Has to be applied to DirectoryModelForms
from mptt.forms import MoveNodeForm

from django import forms
from django.utils.text import get_text_list
from django.utils.encoding import force_unicode


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


class FormsetErrorProcessingMixin(object):
    """
    FormSet with additional error processing functionality.
    """
    def errors_list(self):
        formset_errors = []
        for i, error in filter(lambda x: x[1], list(enumerate(self.errors))):
            for v, k in error.items():
                formset_errors.append(map(lambda x: (("testcasestep_set-%s-%s") % (i, v), x), k)[0])
        return formset_errors

    def _errors_list(self):
        errors = []
        for i, error in  enumerate(self.errors):
            for field, messages in error.items():
                if field == "__all__":
                    errors.append(("%s-%s" % (self.prefix, i), " .".join(messages)))
                else:
                    errors.append(("%s-%s-%s" % (self.prefix, i, field), " .".join(messages)))

        return errors


class FormsetChangelogMixin(object):
    def changelog(self):
        change_message = []

        for added_object in getattr(self, "new_objects", ()):
            change_message.append('Added %(name)s "%(object)s"'
                                  % {'name': force_unicode(added_object._meta.verbose_name),
                                     'object': force_unicode(added_object)})
        for changed_object, changed_fields in getattr(self, "changed_objects", ()):
            change_message.append('Changed %(list)s for %(name)s "%(object)s"'
                                  % {'list': get_text_list(changed_fields, 'and'),
                                     'name': force_unicode(changed_object._meta.verbose_name),
                                     'object': force_unicode(changed_object)})
        for deleted_object in getattr(self, "deleted_objects", ()):
            change_message.append('Deleted %(name)s "%(object)s"'
                                  % {'name': force_unicode(deleted_object._meta.verbose_name),
                                     'object': force_unicode(deleted_object)})

        return "%s." % ', '.join(change_message)


class BaseForm(forms.Form, FormErrorProcessingMixin):
    pass


class BaseModelForm(forms.ModelForm, FormErrorProcessingMixin):

    class Meta:
        pass

    def changelog(self):
        change_message = []
        if self.changed_data:
            change_message.append('Changed %s.' % get_text_list(self.changed_data, 'and'))
        return ''.join(change_message)

    def save(self, *args, **kwargs):
        """
        Save method that allows to chage model's save kwargs
        just for the model save invocation.

        Some of core models allows to change save method behaviour
        by passing some flags arguments.
        """

        model_save_kwargs = kwargs.pop('model_save_kwargs', {})
        original_save = self.instance.save

        def save(*a, **k):
            k.update(model_save_kwargs)
            original_save(*a, **k)

        self.instance.save = save
        self.instance = super(BaseModelForm, self).save(*args, **kwargs)
        self.instance.save = original_save
        return self.instance


class PathModelForm(BaseModelForm):
    class Meta:
        exclude = ("path",)

    def save(self, validate_path_unique=False, *args, **kwargs):
        kwargs['model_save_kwargs'] = {'validate_path_unique': validate_path_unique}
        return super(PathModelForm, self).save(*args, **kwargs)


class DirectoryModelForm(PathModelForm):
    class Meta(PathModelForm.Meta):
        pass


    def __init__(self, *args,**kwargs):
        super(DirectoryModelForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            desc_ids = map(lambda x: x.pk, self.instance.get_descendants())
            self.fields['parent'].queryset =\
                self.instance.__class__.objects.exclude(pk__in=desc_ids).exclude(pk=self.instance.id)


class BaseInlineFormSet(forms.models.BaseInlineFormSet,
                        FormsetErrorProcessingMixin,
                        FormsetChangelogMixin):
    pass


class BaseModelFormSet(forms.models.BaseModelFormSet,
                       FormsetErrorProcessingMixin,
                       FormsetChangelogMixin):
    pass

