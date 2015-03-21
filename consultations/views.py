from django.views.generic import ListView

from .models import Consultation


class ConsultationsListView(ListView):
    model = Consultation
