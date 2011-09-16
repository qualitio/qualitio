from threading import local


# We'll have sure that THREAD object will always have 'project'
# and 'organization' attributes
class ThreadLocal(local):
    project = None
    organization = None


THREAD = ThreadLocal()
