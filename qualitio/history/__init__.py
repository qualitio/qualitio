from reversion import revision

from django.utils.text import get_text_list
from django.utils.encoding import force_unicode


class History(object):

    def __init__(self, user, object, **kwargs):
        self.user = user
        self.forms = map(lambda x: (x, (), False), kwargs.get('forms', ()))
        self.object = object
        self.releated_objects = []
        self.messages = []

    def add_form(self, modelform, capture=[], prefix=False):
        self.forms.append((modelform, capture, prefix))

    def add_formset(self, formset, **kwargs):
        prefix_object = None
        if kwargs.get("prefix", False):
            prefix_object = formset.instance

        objects = {"created": formset.new_objects,
                   "deleted": formset.deleted_objects,
                   "changed": formset.changed_objects,
                   "prefix_object": prefix_object}

        self.releated_objects.append(objects)

    def add_objects(self, **objects):
        self.releated_objects.append(objects)

    def add_message(self, msg):
        self.messages.append(msg)

    def save(self):
        message_parts = []
        for form, capture, prefix in self.forms:
            message_parts.append(self.log_from_form(form, capture, prefix))

        for objects in self.releated_objects:
            message_parts.append(self.log_objects_related(**objects))

        for msg in self.messages:
            message_parts.append(msg)

        message_parts = filter(lambda x:x, message_parts)
        if message_parts:
            return self._log(". ".join(message_parts))
        return ""

    def _log(self, message):
        if message:
            revision.start()
            revision.user = self.user
            revision.comment = "%s." % message
            revision.add(self.object)
            revision.end()
            return message
        return ""

    def log_from_form(self, form, capture=[], prefix=False):
        if self._has_new_object(form):
            return self.log_new_object(form.instance, prefix)
        return self.log_object(form.instance, form.changed_data, capture, prefix)

    def _has_new_object(self, form):
        return not bool(form.initial.get('id', False))

    def log_object(self, obj, fields, capture=[], prefix=False):
        message_parts = []

        for field in fields:
            if field in capture:
                message_parts.append("changed %s to '%s'" % (field, getattr(obj, field)))
            else:
                message_parts.append("changed %s" % field)

        message = get_text_list(message_parts, "and").capitalize()

        if prefix:
            return "%s: %s: %s" % (obj._meta.verbose_name.capitalize(),
                                   obj.pk,
                                   message)

        return message

    def log_new_object(self, obj, prefix=False):
        message = "Object created"

        if prefix:
            return "%s: %s: %s" % (obj._meta.verbose_name.capitalize(),
                                   obj.pk,
                                   message)
        return message

    def log_from_formset(self, formset, **kwargs):
        return self.log_objects_related(formset.instance,
                                        created=formset.new_objects,
                                        deleted=formset.deleted_objects,
                                        changed=formset.changed_objects)


    def log_objects_related(user, **kwargs):
        message_parts = []

        for added_object in kwargs.get("created", ()):
            message_parts.append('added %(name)s "%(object)s"'
                                 % {'name': force_unicode(added_object._meta.verbose_name),
                                    'object': force_unicode(added_object)})

        for changed_object, changed_fields in kwargs.get("changed", ()):
            message_parts.append('changed %(list)s for %(name)s "%(object)s"'
                                 % {'list': get_text_list(changed_fields, 'and'),
                                    'name': force_unicode(changed_object._meta.verbose_name),
                                    'object': force_unicode(changed_object)})

        for deleted_object in kwargs.get("deleted", ()):
            message_parts.append('deleted %(name)s "%(object)s"'
                                 % {'name': force_unicode(deleted_object._meta.verbose_name),
                                    'object': force_unicode(deleted_object)})

        message = get_text_list(message_parts, "and").capitalize()


        prefix_object = kwargs.get("prefix_object", None)
        if prefix_object:
            return "%s: %s: %s" % (prefix_object._meta.verbose_name.capitalize(),
                                   prefix_object.pk,
                                   message)

        return message

