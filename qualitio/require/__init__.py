import reversion
from qualitio import module_absolute_url
from qualitio.require.models import Requirement


if not reversion.is_registered(Requirement):
    reversion.register(Requirement)


get_absolute_url = module_absolute_url(module_name="require")
