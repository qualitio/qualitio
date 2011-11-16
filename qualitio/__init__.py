from threading import local


# We'll have sure that THREAD object will always have 'project'
# and 'organization' attributes
class ThreadLocal(local):
    project = None
    organization = None


THREAD = ThreadLocal()


class module_absolute_url(object):
    """
    Simple object that behavies like a function.
    Usefull to imitate "get_absolute_url" module functions
    in "require", "store", "execute" and "report" modules.

    Eliminates THREAD importing from the code.
    """

    def __init__(self, module_name):
        self.module_name = module_name

    def __call__(self):
        if THREAD.project:
            return "%s%s/" % (THREAD.project.get_absolute_url(), self.module_name)
        return "/%s/" % self.module_name

