from django.contrib import admin

from .models import PaymentStrategy

class PaymentStrategyAdmin(admin.ModelAdmin):
    list_display = ["verbose_name", "price", "users"]
admin.site.register(PaymentStrategy, PaymentStrategyAdmin)