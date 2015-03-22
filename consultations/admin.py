from django.contrib import admin
from django.contrib.admin import site

from .models import Consultation, Topic


class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('title', 'closing_date')
    date_hierarchy = 'closing_date'


class TopicAdmin(admin.ModelAdmin):
    pass


site.register(Consultation, ConsultationAdmin)
site.register(Topic, TopicAdmin)
