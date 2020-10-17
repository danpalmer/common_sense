from django.db import models
from django.views import generic as views

from .enums import ConsultationStateEnum
from .models import Consultation


class HomePageView(views.TemplateView):
    template_name = 'consultations/home.html'

    def get_context_data(self):
        context = super(HomePageView, self).get_context_data()

        context.update({
            state.slug: count for state, count in
            Consultation.objects.values_list(
                'state'
            ).annotate(
                models.Count('id'),
            )
        })

        return context


class ConsultationsListView(views.ListView):
    queryset = Consultation.objects.order_by('state', 'closing_date')


class ConsultationView(views.DetailView):
    model = Consultation
