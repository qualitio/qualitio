"""
Tastypie ModelResource re-definition that adds
automatically generated reverse ``customization`` field.

For models that has customizations it will automatically
register customization model and resource.
"""
from tastypie.resources import ModelResource as TastypieModelResource, ModelDeclarativeMetaclass
from tastypie import fields
from tastypie.api import Api as TastypieApi


def create_customization_model_resource(customization_model):
    cls_name = customization_model.__name__
    app_name = customization_model._meta.app_label

    class Meta:
        queryset = customization_model.objects.all()
        resource_name = '%s/%s' % (app_name, cls_name.lower())

    return type('%sResource' % cls_name, (TastypieModelResource,), {'Meta': Meta})


class CustomizationModelDeclarativeMetaclass(ModelDeclarativeMetaclass):
    def __new__(cls, cls_name, bases, attrs):
        meta = attrs.get('Meta')

        model = getattr(meta, 'object_class', None)
        if not model:
            model = getattr(getattr(meta, 'queryset', None), 'model', None)

        if hasattr(model, '_customization_model'):
            CustomizationModelResource = create_customization_model_resource(model._customization_model)
            attrs['customization'] = fields.ToOneField(CustomizationModelResource,
                                                       'customization', null=True, full=True)
            attrs['CustomizationModelResource'] = CustomizationModelResource

        return super(CustomizationModelDeclarativeMetaclass, cls).__new__(cls, cls_name, bases, attrs)


class ModelResource(TastypieModelResource):
    __metaclass__ = CustomizationModelDeclarativeMetaclass


class Api(TastypieApi):
    def register(self, resource, canonical=True):
        super_register = super(Api, self).register
        CustomizationModelResource = getattr(resource.__class__, 'CustomizationModelResource', None)

        if CustomizationModelResource:
            super_register(CustomizationModelResource(), canonical=canonical)

        super_register(resource, canonical=canonical)

    def unregister(self, resource_name):
        super_unregister = super(Api, self).unregister

        if resource_name in self._registry:
            resource_class = self._registry[resource_name].__class__
            if hasattr(resource_class, 'CustomizationModelResource'):
                super_unregister(resource_class.CustomizationModelResource._meta.resource_name)

        super_unregister(resource_name)
