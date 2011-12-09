from django.contrib import admin

from .models import Strategy, Profile


class StrategyAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "users"]
admin.site.register(Strategy, StrategyAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["organization", "strategy", "status", "paypal_id",
                    "valid_time", "created_time"]
admin.site.register(Profile, ProfileAdmin)