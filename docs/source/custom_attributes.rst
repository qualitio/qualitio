Customizations
==============

Qualitio has ability to customize base models to fit your needs.

``qualitio.core.custommodel``   is   application   that   gives   base
foundation for  model customizations.  By model customization  we mean
easy way  of extending  execute, store and  require models  fields and
also adding your custom validation.

You       don't       need       add      anything       to       your
code. ``qualitio.core.custommodel`` application's models and forms are
already applied to all ``qualitio.core`` models and forms.


How customization works
-----------------------

Each  customization model defines  it's target  (the model  which it
will extend). Here's how it works.

.. _requirement-customization:

.. code-block:: python

  from django.db import models

  from qualitio.core.custommodel.models import ModelCustomization
  from qualitio.require.models import Requirement

  class RequirementCustomization(ModelCustomization):
	mark = models.IntegerField(null=True, blank=True, choices=(
		(1, "Good"),
		(2, "Better"),
		(3, "The best"),
		))

	class Meta:
	    model = Requirement


You're  simply   telling  qualitio  which  model  is   the  target  of
customization  and you're defining  fields on  your ModelCustomization
model.   ModelCustomization  will simply  have  OneToOneField to  your
``model``.

.. note::
   Do  not ever, ever create  ModelCustomization instances by
   your self. It is created (and saved) on every CustomizableModel save so
   you don't need to bother about it.


How add ModelCustomization
--------------------------

There's already installed app ``qualitio.customizations`` where your
model customizations should live.

Following the  example above, you should put  your customization model
in  ``qualitio.customizations.models`` module.  Once  you do  this you
need to type schemamigration & migration commands:

::

  $ ./manage.py schemamigration --add-model=RequirementCustomization customizations
  $ ./manage.py migrate


Every time  you add  new model customizations  run those  commands for
each of them.

If  you  already  have  customizations.models.RequirementCustomization
defined  and you  want to  add new  or remove  existing  field, simply
add/remove one and then type commands:

::

  $ ./manage.py schemamigration customizations --auto
  $ ./manage.py migrate


API
---

Once you define your  ModelCustomization subclass, qualitio detail and
edit views will dynamically extend. There's also following API you
can play with.


.. code-block:: python

  >>> from require.models import Requirement
  >>> req = Requirement.objects.get(id=1)
  >>> req.customization    # direct path to customization object
  >>>
  >>> req.custom_fields()  # returns dict with req.customization object values.
  >>> {'Mark': None }      # It's important that keys are 'verbose_name's
  >>>                      # not just name. And values supports 'choices' options
  >>>                      # (get_<name>_display functions are used).
  >>>
  >>> req.raw_custom_values()  # returns dict with req.customization object values.
  >>> {'mark': None}           # This time keys are just field names, and values
  >>>                          # are returned as they are (no 'choices' support)
