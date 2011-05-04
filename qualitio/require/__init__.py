import reversion

from models import Requirement


if not reversion.is_registered(Requirement):
    reversion.register(Requirement)
