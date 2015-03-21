from django.contrib import admin

from .models import UserTopic


class UserTopicAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserTopic, UserTopicAdmin)
