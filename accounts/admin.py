from django.contrib import admin
from accounts import models as account_models


@admin.register(account_models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "role", "is_active"]
    list_filter = ["role"]
    search_fields = ["username"]
