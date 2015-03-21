from django.views import generic as views

from .models import Consultation


class HomePageView(views.TemplateView):
    template_name = 'consultations/home.html'


class ConsultationsListView(views.ListView):
    model = Consultation
