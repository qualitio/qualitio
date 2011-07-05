# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.forms.forms import BoundField


def should_be_excluded(name, fields, exclude):
    return bool((fields and not name in fields) or (exclude and name in exclude))


class CustomizableModelFormMetaclass(forms.models.ModelFormMetaclass):
    def __new__(cls, name, bases, attrs):
        model_form = super(CustomizableModelFormMetaclass, cls).__new__(cls, name, bases, attrs)
        opts = model_form._meta

        if hasattr(opts.model, '_customization_model'):
            for field in opts.model._customization_model._custom_meta.get_custom_fields():
                # NOTE: we don't check "fields" because we do not support it right now
                if should_be_excluded(field.name, None, opts.exclude):
                    continue
                model_form.base_fields[field.name] = field.formfield()

        return model_form


class CustomizableModelForm(forms.ModelForm):
    __metaclass__ = CustomizableModelFormMetaclass

    def _custom_fields_meta(self):
        if not hasattr(self._meta.model, '_customization_model'):
            return []
        return self._meta.model._customization_model._custom_meta.get_custom_fields()

    def _construct_instance(self):
        instance = forms.models.construct_instance(
            self, self.instance, self._meta.fields, self._meta.exclude)

        if hasattr(self._meta.model, '_customization_model'):
            # All do we need here is just to setup instance.customization fields
            # validation on this will be trigered by instance.full_clean validation
            for field in self._custom_fields_meta():
                setattr(instance.customization, field.name, self.cleaned_data.get(field.name))
            # NOTE: self.cleaned_data.get method is used here intentionally. Even if it
            #       returns None the instance.full_clean method will check it.

        return instance

    def _post_clean(self):
        # Update the model instance with self.cleaned_data.
        self.instance = self._construct_instance()

        # From here ** THIS ** is exact copy of super _post_clean method.
        # We had to change the way of construction to make our live easier.

        exclude = self._get_validation_exclusions()

        # Foreign Keys being used to represent inline relationships
        # are excluded from basic field value validation. This is for two
        # reasons: firstly, the value may not be supplied (#12507; the
        # case of providing new values to the admin); secondly the
        # object being referred to may not yet fully exist (#12749).
        # However, these fields *must* be included in uniqueness checks,
        # so this can't be part of _get_validation_exclusions().
        for f_name, field in self.fields.items():
            if isinstance(field, forms.models.InlineForeignKeyField):
                exclude.append(f_name)

        # Clean the model instance's fields.
        try:
            self.instance.clean_fields(exclude=exclude)
        except ValidationError, e:
            self._update_errors(e.message_dict)

        # Call the model instance's clean method.
        try:
            self.instance.clean()
        except ValidationError, e:
            self._update_errors({NON_FIELD_ERRORS: e.messages})

        # Validate uniqueness if needed.
        if self._validate_unique:
            self.validate_unique()


    def custom_fields(self):
        field_names = map(lambda f: f.name, self._custom_fields_meta())
        for name, field in [(n, self.fields[n]) for n in field_names]:
            yield BoundField(self, field, name)
