from django.contrib import admin
from .models import Messages, messages_sent, Campaign
from mail.models import EmailAudience


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'tag', 'count')
    list_filter = ('user', 'message', 'tag')

# Register the Campaign model with the custom admin
admin.site.register(Campaign, CampaignAdmin)



# Custom Admin for Messages
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subject', 'content_type', 'massenger', 'date_time')
    search_fields = ('subject', 'user__username', 'massenger')
    list_filter = ('content_type', 'massenger', 'date_time')
    ordering = ('-date_time',)

    # Customizing form fields in the admin panel
    fieldsets = (
        (None, {
            'fields': ('user', 'subject', 'content_type', 'content', 'massenger')
        }),
        # Date field is excluded from the form since it's auto-generated
    )

# Custom Admin for messages_sent
class MessagesSentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'interacted_users', 'platform', 'date_time')
    search_fields = ('user__username', 'message__subject', 'platform')
    list_filter = ('platform', 'date_time')
    ordering = ('-date_time',)
    readonly_fields = ('user', 'message', 'interacted_users', 'platform', 'date_time')

    # Inline display of related message details
    raw_id_fields = ('message',)
    autocomplete_fields = ['user']

    # Custom form layout
    fieldsets = (
        (None, {
            'fields': ('user', 'message', 'interacted_users', 'platform')
        }),
    )

# Register the models with the admin interface
admin.site.register(Messages, MessagesAdmin)
admin.site.register(messages_sent, MessagesSentAdmin)
