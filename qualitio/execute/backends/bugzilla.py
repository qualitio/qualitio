import httplib2
from xml.dom import minidom
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class IssueError(Exception):
    pass


class IssueServerError(Exception):
    pass


class Backend(object):
    resource = None
    url = ""

    @classmethod
    def _setup_connection(cls):
        if hasattr(settings, "ISSUE_BACKEND_BUGZILLA_URL"):
            cls.url = settings.ISSUE_BACKEND_BUGZILLA_URL.rstrip("/")
        else:
            raise ImproperlyConfigured("Bugzilla issue backed requires ISSUE_BACKEND_BUGZILLA_URL value in settings")

        login = getattr(settings, "ISSUE_BACKEND_BUGZILLA_USER", "")
        password = getattr(settings, "ISSUE_BACKEND_BUGZILLA_PASSWORD", "")
        cls.resource = httplib2.Http()
        if login:
            cls.resource.add_credentials(login, password)

    @classmethod
    def fetch_bug(cls, bug_id):
        if not cls.resource:
            cls._setup_connection()
        try:
            resp, content = cls.resource.request(
                "%s/show_bug.cgi?id=%s&ctype=xml" % (cls.url, bug_id))

        except httplib2.ServerNotFoundError, e:
            raise IssueServerError(e)
        if resp['status'] == "200":
            return cls._parse_response(content)
        raise IssueServerError(
            u"Unable to connect the server at %s, status code %s" %
            (cls.url, resp['status']))

    @classmethod
    def _parse_response(self, content):
        node = minidom.parseString(content)

        error = node.getElementsByTagName("bug")[0].getAttribute("error")
        if error:
            raise IssueError(error)

        bug = {}
        bug['alias'] = node.getElementsByTagName("bug_id")[0].firstChild.data
        bug['name'] = node.getElementsByTagName("short_desc")[0].firstChild.data
        bug['status'] = node.getElementsByTagName("bug_status")[0].firstChild.data
        bug['resolution'] = node.getElementsByTagName("resolution") or ""
        if bug['resolution']:
            bug['resolution'] = bug['resolution'][0].firstChild.data

        return bug
