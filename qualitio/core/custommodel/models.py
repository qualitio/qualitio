# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ImproperlyConfigured, ValidationError


# the origin model should inherit from CustomizableModel class
class CustomizableModel(models.Model):
    class Meta:
        abstract = True

    def has_customization(self):
        return hasattr(self, '_customization_model')

    def full_clean(self, exclude=None, clean_customization=True):
        errors = {}

        try:
            super(CustomizableModel, self).full_clean(exclude=exclude)
        except ValidationError as e:
            errors = e.update_error_dict(errors)

        if self.has_customization() and clean_customization:
            try:
                self.customization.clean_origin()
            except ValidationError as e:
                errors = e.update_error_dict(errors)

        if errors:
            raise ValidationError(errors)

    def save(self, force_insert=False, force_update=False, using=None, save_customization=True):
        super(CustomizableModel, self).save(
            force_update=force_update, force_insert=force_insert, using=using)
        if self.has_customization() and save_customization:
            self.customization.origin = self
            self.customization.save()


class CustomRelatedObjectDescriptor(models.fields.related.SingleRelatedObjectDescriptor):
    def __get__(self, instance, instance_type):
        try:
            return super(CustomRelatedObjectDescriptor, self).__get__(instance, instance_type)
        except self.related.model.DoesNotExist:
            customization = self.related.model(origin=instance)
            setattr(instance, self.cache_name, customization)
            return customization


# the customization model of the origin model should have
# CustomizationTarget build-in
class CustomizationTarget(models.fields.related.OneToOneField):
    def contribute_to_related_class(self, cls, related):
        setattr(cls, related.get_accessor_name(),
                CustomRelatedObjectDescriptor(related))


class Options(object):
    def __init__(self, Meta):
        # setup
        self.customization_target = Meta.customization_target

        # cleanup
        del Meta.customization_target

        # this will be setup in __new__ of metaclass
        self.customization_model = None

    def _field_filter(self, f):
        return f.name != 'origin' and not isinstance(f, models.AutoField)

    # This will be handy shortcut for things like CustomizableModelForm
    def get_custom_fields(self):
        return filter(self._field_filter, self.customization_model._meta.fields)


# TODO: There can be one and only one customization model for each model
class ModelCustomizationMetaclass(models.base.ModelBase):
    def __new__(cls, name, bases, attrs):
        Meta = attrs.get('Meta')
        custom_meta = None

        if Meta is not None:
            if hasattr(Meta, 'customization_target'):
                custom_meta = Options(Meta)
                if custom_meta.customization_target is not None:
                    attrs['_custom_meta'] = custom_meta
                    attrs['origin'] = CustomizationTarget(custom_meta.customization_target, related_name='customization')

        new_model = super(ModelCustomizationMetaclass, cls).__new__(cls, name, bases, attrs)
        if custom_meta is not None:
            custom_meta.customization_model = new_model
            custom_meta.customization_target._customization_model = new_model

        # TODO: for migration reason - should we check
        #       if there all ModelCustomization fields has blank==True?

        return new_model


class ModelCustomization(models.Model):
    __metaclass__ = ModelCustomizationMetaclass

    class Meta:
        abstract = True

    def _clean_origin(self):
        if self.origin.pk is not None:
            self.clean_origin()

    def clean_origin(self):
        pass

    def full_clean(self, clean_origin=True):
        errors = {}

        try:
            super(ModelCustomization, self).full_clean()
        except ValidationError as e:
            errors = e.update_error_dict(errors)

        if clean_origin:
            try:
                self.clean_origin()
            except ValidationError as e:
                errors = e.update_error_dict(errors)

        if errors:
            raise ValidationError(errors)
