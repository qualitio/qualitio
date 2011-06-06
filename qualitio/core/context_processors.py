import uuid
from django.utils.formats import get_format
from django.utils.safestring import mark_safe
from django.conf import settings as global_settings

def settings(request):
    # conversion between python and javaScript date(time) formats
    format = get_format('DATE_FORMAT')
    format = format.replace('d', 'dd').replace('m', 'mm').replace("Y","yy")
    return {'DATE_FORMAT' : mark_safe('"%s"' % format),
            'AUTH_AUTO_LOGIN': getattr(global_settings, "AUTH_AUTO_LOGIN", "")}

def development(request):
    static_content_hash = ""
    if global_settings.DEBUG:
        static_content_hash = uuid.uuid4()

    return { "STATIC_HASH" : "?%s" % static_content_hash }

def core(request):
    from django.core.urlresolvers import resolve

    http_protocol = "http"
    if request.is_secure():
        http_protocol += "s"

    return { "CURRENT_MODULE" : resolve(request.path).app_name,
             "HTTP_PROTOCOL": http_protocol }
