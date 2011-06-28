# -*- coding: utf-8 -*-
import re

from django.core.exceptions import ValidationError, FieldError
from django.template import Context, Template, TemplateSyntaxError
from django.db.models import query, loading
from django.views import debug


ALLOWED_OBJECTS = ["TestCase", "TestCaseRun", "TestRun", "Report", "Requirement", "Bug"]
ALLOWED_METHODS = ["all", "get", "filter", "exclude", "order_by", "reverse", "count"]
ALLOWED_APPS = ["require", "store", "execute", "report"]


def clean_query_string(query):
    query_segments = query.split(".")
    if len(query_segments) < 2:
        raise ValidationError({"query": "Minimal query should be: ObjectType.method([key=value])"})

    valid_object, methods = query_segments[0], query_segments[1:]
    if valid_object not in ALLOWED_OBJECTS:
        raise ValidationError({"query": "Type '%s' is not supported" % valid_object})

    valid_methods = []
    for method in methods:
        method_re = re.match("(?P<method>\w+)\((?P<args>(\w+=.+)?)\)$", method)

        try:
            method_name = method_re.groupdict()["method"]
            try:
                args = dict([(method_re.groupdict()["args"].split("=")[0],
                              method_re.groupdict()["args"].split("=")[1].strip('"').strip("'"))])
            except IndexError:
                args = dict()
        except AttributeError:
            raise ValidationError({"query": "Method '%s' is in wrong format" % method})

        if method_name not in ALLOWED_METHODS:
            raise ValidationError({"query": "Method '%s' is unsupported" % method_name})

        valid_methods.append((method_name, args))

    return build_query(valid_object, valid_methods)

def get_model(model_name):
    for app in ALLOWED_APPS:
        Model = loading.get_model(app, model_name)
        if Model:
            return Model
    return None

def build_query(model_name, methods):
    """
    build_query method evaluates query starting with
    primitives:

    build_query(
        "Person",
        [('filter', {'name': 'Some name', 'last_name': 'Some last name'}),
         ('exclude', {'id': 1 }),
        ])

    It returns one of following:
    1) queryset (if the last invoked method was: filter, exclude, order_by, reverse)
    2) model_instance (if the last invoked method was: get)
    3) number (if the last invoked method was: count)
    """

    Model = get_model(model_name)
    if not Model:
        return query.QuerySet()

    queryset = Model.objects.all()
    for name, kwargs in methods:
        try:
            queryset = getattr(queryset, name)(**kwargs)
        except Model.DoesNotExist:  # in case of using 'get' method
            return None
        except FieldError as e:
            raise ValidationError({"query": repr(e) })

    return queryset


class ReportValidator(object):
    """
    Custom report and context validator.
    Usage:

    validator = ReportValidator("{% for e in elements %}<p>{{ e.name }}</p>{% endfor %}", {
        "elements": "TestCase.all()",
    })

    OR:

    validator = ReportValidator("{% for e in elements %}<p>{{ e.name }}</p>{% endfor %}", {
        "elements": TestCase.objects.all(),  # real queryset objects
    })

    Validation goes this way:
    1) First 'query_strings' are validated, errors are stored in 'errors' attribute (dict).
    2) Then those queries are evaluated and stored in 'queries' attribute.
       If there is any error it is stored in 'errors' attribute.
    3) In the end the whole template is evaluated with the 'queries'.
       If there is any error it is stored in 'errors' attribute.

    If validation is OK there's an 'queries' dictionary attribute with QuerySet's objects results.
    """

    def __init__(self, template_string, context_queries):
        self.template_string = template_string
        self.context_queries = context_queries
        self.errors = {}
        self.queries = {}

    def is_valid(self):
        for name, query in self.context_queries.items():
            try:
                self.queries[name] = self.clean_query(query)
            except ValidationError as e:
                self.errors = e.update_error_dict(self.errors)

        try:
            self.clean_template(self.template_string, self.queries)
        except ValidationError as e:
            self.errors = e.update_error_dict(self.errors)

        return not bool(self.errors)

    def clean_query(self, query):
        if isinstance(query, basestring):
            return clean_query_string(query)
        return query

    def clean_template(self, template_string, context):
        try:
            unicode(Template(template_string).render(Context(context)))
        except TemplateSyntaxError as e:
            raise ValidationError({"template": self._format_template_error_msg(e)})

    def _get_template_exception_info(self, exception):
        origin, (start, end) = exception.source
        template_source = origin.reload()
        upto = line = 0
        for num, next in enumerate(debug.linebreak_iter(template_source)):
            if start >= upto and end <= next:
                line = num
            upto = next
        return line

    def _format_template_error_msg(self, e):
        return 'Line %s: %s' % (self._get_template_exception_info(e), e)
