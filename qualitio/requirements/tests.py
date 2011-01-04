from nose.tools import *

from qualitio.requirements.models import Requirement, RequirementDependency

def requirements_save():
    requirement = Requirement.objects.create(name="req1")
    requirement_dependency = RequirementDependency.objects.get(root=requirement)
    assert requirement, requirement_dependency.root
