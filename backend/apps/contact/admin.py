from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['status']
    readonly_fields = ['name', 'email', 'subject', 'message', 'ip_address', 'created_at']

    def has_add_permission(self, request):
        return False  # Messages come from the contact form only
