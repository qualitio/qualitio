from django.db import models


class Strategy(models.Model):
    name = models.CharField(max_length=64)
    users = models.IntegerField()
    price = models.FloatField(default=0)

    def endpayment(self):
        pass

    def __unicode__(self):
        return self.name

    @classmethod
    def get_default(cls):
        try:
            return cls.objects.all()[0]
        except IndexError:
            return cls.objects.create(
                name="Free",
                users=5,
                price=0
            )

class Profile(models.Model):
    organization = models.OneToOneField('organizations.Organization',
                                        related_name="payment")
    strategy = models.OneToOneField('Strategy')
    paypal_id = models.CharField(max_length=14, blank=True)

    INACTIVE = 0
    PENDING = 1
    ACTIVE = 2
    CANCELED = 3
    
    choices = (
        (INACTIVE, "Inactive"),
        (PENDING, "Pending"),
        (ACTIVE, "Active"),
        (CANCELED, "Canceled")
    )
    
    status = models.PositiveSmallIntegerField(choices=choices, default=0)
    valid_time = models.DateTimeField()
    created_time = models.DateTimeField()

    def __unicode__(self):
        return "%s :%s" % (self.organization.name,
                           self.strategy.name)

    def is_running(self):
        return self.status in (self.PENDING, self.ACTIVE)
