from django.utils.formats import get_format
from django.utils.safestring import mark_safe

def settings(request):
    return {'DATE_FORMAT' : mark_safe('"%s"' % get_format('DATE_FORMAT').replace("%","").replace("y","yy"))}
