from django.contrib import admin
from .models import Private_Message


class MessageAdmin(admin.ModelAdmin):
    class Meta:
        model = Private_Message




admin.site.register(Private_Message, MessageAdmin)
