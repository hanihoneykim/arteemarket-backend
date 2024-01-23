from django.contrib import admin
from .models import User, Participant, Purchase


class UserAdmin(admin.ModelAdmin):
    search_fields = ["email"]


admin.site.register(User, UserAdmin)
admin.site.register(Participant)
admin.site.register(Purchase)
