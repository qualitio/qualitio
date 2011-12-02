from django.db import models


class Strategy(models.Model):
    name = models.CharField(max_length=64)
    users = models.IntegerField()
    price = models.FloatField(default=0)

    def endpayment(self):
        pass

    def __unicode__(self):
        return self.name


class Profile(models.Model):
    organization = models.OneToOneField('organizations.Organization',
                                        related_name="payment")
    strategy = models.OneToOneField('Strategy')
    paypal_id = models.CharField(max_length=14, blank=True)

    status = models.BooleanField()
    valid_till = models.DateField()

    def __unicode__(self):
        return "%s :%s" % (self.organization.name,
                           self.strategy.name)
