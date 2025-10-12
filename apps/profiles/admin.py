from django.contrib import admin
from .models import Profile, Role

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "get_roles", "is_active", "active")
    list_filter = ("roles", "is_active", "active")
    search_fields = ("user__username", "user__email", "phone")
    filter_horizontal = ("practice_areas", "assigned_lawyers", "roles")

    def get_roles(self, obj):
        return ", ".join(obj.roles.values_list('name', flat=True)) or "-"
    get_roles.short_description = "Roles"

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Role)
