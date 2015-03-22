from django.contrib import admin
from django.contrib.admin import site

from .models import UserTopic


class UserTopicAdmin(admin.ModelAdmin):
    pass


site.register(UserTopic, UserTopicAdmin)
