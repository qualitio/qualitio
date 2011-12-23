from django.db import models
from .paypal import PayPal, PayPalException


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
    strategy = models.ForeignKey('Strategy')
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

    def __init__(self, *args, **kwargs): 
        super(Profile, self).__init__(*args, **kwargs) 
        self._status = self.status
        self._strategy = self.strategy
    
    def __unicode__(self):
        return "%s :%s" % (self.organization.name,
                           self.strategy.name)

    def is_running(self):
        return self.status in (self.PENDING, self.ACTIVE)

    def cancel(self):
        if self._status in (Profile.PENDING, Profile.ACTIVE):
            try:
                paypal = PayPal()
                paypal.ManageRecurringPaymentsProfileStatus(
                    PROFILEID=self.paypal_id,
                    ACTION="Cancel")
            except PayPalException as e:
                # thats allright, profile was cancled again
                if e.message['L_ERRORCODE0'] not in ('11556', '11551'): 
                    raise e

            if self._status == Profile.PENDING:
                self.status = Profile.INACTIVE
                self.strategy = Strategy.get_default()
                self.paypal_id = ""

            if self._status == Profile.ACTIVE:
                self.status = Profile.CANCELED

            self.save(cancel_check=False)
            
        
    def save(self, **kwargs):
        admin_memeber = kwargs.pop('admin_memeber', None)
        
        if self._strategy != self.strategy and \
            self._strategy.users > self.strategy.users:
            
            from qualitio.organizations.models import OrganizationMember

            members = OrganizationMember.objects.filter(organization=self.organization)
            
            admins = members.filter(role=OrganizationMember.ADMIN)
            others = members.exclude(role=OrganizationMember.ADMIN)

            others.update(role=OrganizationMember.INACTIVE)
            
            if admin_memeber:
                admins.exclude(pk=admin.pk).update(role=OrganizationMember.INACTIVE)
            else:
                first_admin = admins[:1].values_list("id", flat=True)
                admins.exclude(pk__in=first_admin).update(
                    role=OrganizationMember.INACTIVE)

        cancel_check = kwargs.pop('cancel_check', True)
        if self.status == self.CANCELED and cancel_check:
            self.cancel()
        else:
            super(Profile, self).save(**kwargs)

