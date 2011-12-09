from django import forms

from . import countries

class PaymentForm(forms.Form):
    choices = (
        ("Visa","Visa"),
        ("MasterCard","MasterCard"),
        ("Discover", "Discover"),
        ("Amex", "Amex"),
    )
    plan = forms.CharField(widget=forms.HiddenInput)

    CREDITCARDTYPE = forms.ChoiceField(choices=choices, label="Type", required=True)
    ACCT = forms.DecimalField(label="Number", required=True)
    EXPDATE = forms.CharField(label="Expiration date", required=True)
    CVV2 = forms.CharField(label="CCV", required=True)

    FIRSTNAME = forms.CharField(label="Firstname", required=True)
    LASTNAME = forms.CharField(label="Lastname", required=True)
    STREET = forms.CharField(label="Address", required=True)
    CITY = forms.CharField(label="City", required=True)
    STATE = forms.CharField(label="State/Area/Region", required=True)
    ZIP = forms.CharField(label="Zip", required=True)
    COUNTRYCODE = forms.ChoiceField(choices=countries.COUNTRIES, label="Country", required=True)
