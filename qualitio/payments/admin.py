from django.contrib import admin

from .models import Strategy, Profile


class StrategyAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "users"]
admin.site.register(Strategy, StrategyAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["organization", "strategy", "paypal_id", "valid_till"]
admin.site.register(Profile, ProfileAdmin)