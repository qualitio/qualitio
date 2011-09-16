from qualitio import THREAD
from models import Word, Language, Representation

def get_absolute_url():
    project = getattr(THREAD, "project", None)
    if project:
        return "%s%s/" % (THREAD.project.get_absolute_url(),
                          "glossary")
    return "/glossary/"
