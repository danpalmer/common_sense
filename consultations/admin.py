from django.contrib import admin

from .models import Consultation, Topic


class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('title', 'closing_date')
    date_hierarchy = 'closing_date'


class TopicAdmin(admin.ModelAdmin):
    pass


admin.site.register(Consultation, ConsultationAdmin)
admin.site.register(Topic, TopicAdmin)
