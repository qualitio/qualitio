# Has to be applied to DirectoryModelForms
from mptt.forms import MoveNodeForm

from django import forms
from django.utils.text import get_text_list
from django.utils.encoding import force_unicode
from qualitio.core.custommodel.forms import CustomizableModelForm


class FormErrorProcessingMixin(object):
    def _get_prefix(self):
        if self.prefix:
            return "%s-" % self.prefix
        return ""

    def errors_list(self, additional=()):
        """
        Returns all errors as list of tuples: (field_name, first_of_field_errors).
        Errors can be extended with 'additional' error list.
        """
        additional_errors = additional or ()
        errors = [("%s%s" % (self._get_prefix(), fname), errors[0]) for fname, errors in self.errors.items()]
        errors += list(additional_errors)
        return errors

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


class QuerySetRefreshMixin(object):
    def _refresh_fields_querysets(self):
        for name, field in self.fields.items():
            if hasattr(field, "queryset"):
                field.queryset = field.queryset.model.objects.all()


class BaseForm(forms.Form, FormErrorProcessingMixin, QuerySetRefreshMixin):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        self._refresh_fields_querysets()


class BaseModelForm(CustomizableModelForm, FormErrorProcessingMixin, QuerySetRefreshMixin):
    class Meta:
        exclude = ('project',)

    def __init__(self, *args, **kwargs):
        super(BaseModelForm, self).__init__(*args, **kwargs)
        self._refresh_fields_querysets()

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
    class Meta(BaseModelForm.Meta):
        exclude = ("path",) + BaseModelForm.Meta.exclude

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

