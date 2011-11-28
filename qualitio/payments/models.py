from django.db import models


class PaymentStrategy(models.Model):
    name = models.CharField(max_length=64)
    verbose_name = models.CharField(max_length=64)
    users = models.IntegerField()
    price = models.FloatField(default=0)

    def endpayment(self):
        pass

    def __unicode__(self):
        return self.verbose_name