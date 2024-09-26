from django.contrib import admin
from .models import *
from django.contrib import messages
from django.utils.translation import ngettext

# Admin class for EmailAccounts
@admin.register(EmailAccounts)
class EmailAccountsAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'date_time')
    search_fields = ('email', 'user__username')
    list_filter = ('date_time',)


# Admin class for EmailAudience
@admin.register(EmailAudience)
class EmailAudienceAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'tag', 'date_time')
    search_fields = ('email', 'user__username')
    list_filter = ('date_time','tag')

admin.site.register(EmailClientDataUpload)
# Admin class for EmailClientData
@admin.register(EmailClientData)
class EmailClientDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_time')
    search_fields = ('csv_file', 'user__username')
    list_filter = ('is_valid', 'date_time')
    actions = ['validate_email_data']

    def has_change_permission(self, request, obj=None):
        return False

    # Custom display for user without linking to the change form
    def user_display(self, obj):
        return obj.user.username

    user_display.short_description = 'User'

    # Disable the clickable link in the list display
    def get_list_display_links(self, request, list_display):
        return None


    # Custom action to validate email client data
    @admin.action(description='Validate selected email data')
    def validate_email_data(self, request, queryset):
        for obj in queryset:
            # Implement validation logic here
            if obj.is_valid:
                messages.info(request, f"File {obj.csv_file.name} is already valid.")
            else:
                obj.is_valid = True
                obj.save()
                messages.success(request, f"File {obj.csv_file.name} has been validated successfully.")
