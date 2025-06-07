from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Maid

# Unregister the User model if it's already registered
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# Re-register User with the default UserAdmin
admin.site.register(User, UserAdmin)

# Register Maid model
@admin.register(Maid)
class MaidAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_name', 'get_contact')
    search_fields = ('id',)
    
    def get_name(self, obj):
        return str(obj)
    get_name.short_description = 'Name'
    
    def get_contact(self, obj):
        if hasattr(obj, 'email'):
            return obj.email
        if hasattr(obj, 'phone'):
            return obj.phone
        return '-'
    get_contact.short_description = 'Contact'
