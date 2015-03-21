<<<<<<< HEAD
from django.views.generic import ListView

from .models import Consultation


class ConsultationsListView(ListView):
    model = Consultation
=======
from django.shortcuts import render
from django.views.generic import base as base_views


class HomePageView(base_views.TemplateView):
    template_name = 'consultations/home.html'
>>>>>>> origin/master
