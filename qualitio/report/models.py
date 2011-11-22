from django.core.exceptions import ValidationError
from django.template import Context, Template
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType

from qualitio import core
from qualitio.report import validators


class ReportDirectory(core.BaseDirectoryModel):
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Report directories'


class Report(core.BasePathModel):
    template = models.TextField(blank=True)
    public = models.BooleanField()
    link = models.URLField(blank=True, verify_exists=False)
    MIME_CHOICES = (('text/html', 'html'),
                    ('application/xml', 'xml'),
                    ('application/json', 'json'),
                    ('text/plain', 'plain'))
    mime = models.CharField(blank=False, max_length=20, choices=MIME_CHOICES,
                            default="text/html", verbose_name="format")
    limit_choices_to = {'model__in': ["testcase", "requirement", "testrun"]}
    bound_type = models.ForeignKey(ContentType, blank=True, null=True,
                                   limit_choices_to=limit_choices_to)

    class Meta(core.BasePathModel.Meta):
        parent_class = 'ReportDirectory'
        for_parent_unique = True

    def __init__(self, *args, **kwargs):
        super(Report, self).__init__(*args, **kwargs)
        self.bound_id = None

    def materialize(self, bound_id):
        self.bound_id = bound_id

    @property
    def context_dict(self):
        context_dict = {}
        for context_element in self.context.all():
           context_dict[context_element.name] = context_element.build(self.bound_id)
        return context_dict

    def content(self, request=None):
        template = Template(self.template)
        context = Context(self.context_dict)

        if request:
            context.update({
                    'self': {
                        'user': {
                            'name': request.user.username,
                            'first_name': request.user.first_name,
                            'last_name': request.user.last_name,
                            'email': request.user.email,
                            }
                        }})

        return template.render(context)

    def is_html(self):
        return self.mime == "text/html"

    def is_bound(self):
        return True if self.bound_type else False

    def bound_link(self):
        link_elements = self.link.split("/")
        link_elements.insert(1, str(self.bound_id))
        link_elements.insert(1, str(self.bound_type_id))
        return "/".join(link_elements)

    def save(self, *args, **kwargs):
        # significant part of this link is only ID, rest is only for information purposes.
        # Filter applayed to get rid root's empty path
        if not self.pk:
            super(Report, self).save(*args, **kwargs)

        link_elements = filter(lambda x:x, ['report/external',
                                            str(self.pk),
                                            slugify(self.parent.path),
                                            slugify(self.parent.name),
                                            slugify(self.name),
                                            self.created_time.strftime("%Y/%m/%d")])

        self.link = "%s%s" % (self.project.get_absolute_url(), "/".join(link_elements))
        kwargs['force_insert'] = False
        super(Report, self).save(*args, **kwargs)


class ContextElement(models.Model):
    report = models.ForeignKey("Report", related_name="context")
    name = models.CharField(max_length=512)
    query = models.TextField()

    def full_clean(self):
        """
        full_clean starts the base class full_clean validation and
        also adds 'clean_query' validation.

        Construction of the method looks like this, because 'full_clean'
        should return ALL validation errors, not just a part.
        """
        errors = {}

        try:
            super(ContextElement, self).full_clean()
        except ValidationError as e:
            errors = e.update_error_dict(errors)

        try:
            self.clean_query()
        except ValidationError as e:
            errors = e.update_error_dict(errors)

        if errors:
            raise ValidationError(errors)

    def clean_query(self):
        """
        clean_query validates query string
        """
        validators.clean_query_string(self.query)

    def build(self, bound_id=None):
        if bound_id:
            return validators.clean_query_string(self.query, bound_id)
        else:
            return validators.clean_query_string(self.query)
