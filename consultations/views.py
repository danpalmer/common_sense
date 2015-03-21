from django.views import generic as views

from .models import Consultation


class HomePageView(views.TemplateView):
    template_name = 'consultations/home.html'


class ConsultationsListView(views.ListView):
    queryset = Consultation.objects.order_by('state', 'closing_date')

class ConsultationView(views.DetailView):
    model = Consultation
