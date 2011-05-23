from django.db import models
from django.core.exceptions import ValidationError

from qualitio import core
from qualitio.require import validators, managers


class Requirement(core.BaseDirectoryModel):
    """
    This doc assumes you're familiar with django docs at
    http://docs.djangoproject.com/en/dev/ref/models/instances/#validating-objects

    Implementation of Requirement have three basic abilities:
    * it has additional clean method (clean_dependencies) which checks if there's no
      dependency cycles
    * this additional clean procedure is invoked by 'full_clean' by default.
      First the standard 'full_clean' method is called and then additional
      'clean_dependencies' method is called.
    * calling 'save' doesn't call 'full_clean' but it calls 'clean_dependencies' by
      default

    The reason of this beaviour is to make API safe in case when cycles dependencies
    will be added by a mistake. This means that each time the 'save' method is
    called the 'clean_dependencies' is also called, so the saving operation can take
    awhile. But this is the price for dependency with no cycles safety.
    """

    dependencies = models.ManyToManyField("Requirement", related_name="blocks", null=True, blank=True)
    release_target = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    alias = models.CharField(max_length=512, blank=True) # Unique check in clean method
    objects = managers.RequirementManager()

    def save(self, clean_dependencies=True, *args, **kwargs):
        """
        save method calls 'clean_dependencies' by default, but this can
        be ommited by passing extra keyword argument clean_dependencies=False. So:

        instance = Requirement(...)
        instance.save()                         # this line will call 'clean_dependencies', but...
        instance.save(clean_dependencies=False) # ...but this line won't call the method

        The ability to not checking dependency cycles has been made for situations
        like interaction with forms: when operation could be called more then one time.
        """
        if clean_dependencies:
            self.clean_dependencies()
        super(Requirement, self).save(*args, **kwargs)


    def clean(self):
        if self.alias and not self.pk:
            if Requirement.objects.filter(alias=self.alias).exists():
                raise ValidationError({'alias': "column alias is not unique"})


    def full_clean(self, clean_dependencies=True, exclude=None):
        """
        This method exists for consistency of django Model validation functionality.
        We need this to make sure that model validation checks also the
        dependency cycles.

        Like in 'save' method you can pass clean_dependencies=False
        to skip dependency cycles check.
        """
        errors = {}

        try:
            super(Requirement, self).full_clean(exclude=None)
        except ValidationError, e:
            errors = e.update_error_dict(errors)

        if clean_dependencies:
            try:
                self.clean_dependencies()
            except ValidationError, e:
                errors = e.update_error_dict(errors)

        if errors:
            raise ValidationError(errors)


    def clean_dependencies(self, extra_dependencies=()):
        """
        Checks the dependency cycle.
        Raises ValidationError with 'message_dict' when cycle has been found.

        There is ability to check additional dependencies by passing
        'extra_dependencies' kwarg. For example, when you want to check
        if the dependencies you want to add can be safely saved.

        IMPORTANT: this will NOT work for newly created (and not saved) objects.
        That's because we cannot save dependency connections between unexisted
        (in database) objects.
        """
        # We don't want / cannot to check just created objects
        if self.id:
            dependencies = list(r for r in self.dependencies.all())
            dependencies += list(extra_dependencies)

            validator = validators.RequirementDependencyValidator(self, dependencies)
            if not validator.is_valid():
                raise ValidationError({'dependencies': [validator.format_error_msg()]})
