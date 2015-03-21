from django.contrib import admin

from .models import Consultation


class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('title', 'closing_date')
    date_hierarchy = 'closing_date'


admin.site.register(Consultation, ConsultationAdmin)
