from django import template
from django.template import RequestContext

register = template.Library()


@register.tag
def application_view_menu(parser, token):
    obj, view = token.split_contents()[1:]
    return ApplicationViewMenuNode(parser.compile_filter(obj), parser.compile_filter(view))


class ApplicationViewMenuNode(template.Node):
    def __init__(self, obj, view):
        self.obj = obj
        self.view = view

    def registred_views(self, obj, user, organization):
        from qualitio.core.views import registry

        views = []
        for view in registry.get(obj.__class__, None):
            from qualitio.projects.models import OrganizationMember

            if view['role']:
                role = getattr(OrganizationMember, view['role'], 999999)
                perm=organization.members.filter(user=user, role__lte=role).exists()
                views.append(dict(name=view['name'],
                                  perm=perm))
            else:
                views.append(dict(name=view['name'],
                                  perm=True))
        return views

    def render(self, context):

        materialized_obj = self.obj.resolve(context)
        materialized_view = self.view.resolve(context)
        module_name = materialized_obj._meta.module_name

        return template.loader.render_to_string("core/application_view_menu.html",
                                                {"obj": materialized_obj,
                                                 "current_view": materialized_view,
                                                 "registred_views": self.registred_views(materialized_obj,
                                                                                         context['user'],
                                                                                         context['request'].organization),
                                                 "module_name": module_name},
                                                context_instance=RequestContext(context['request']))
