from django.shortcuts import render
from django.views.generic import base as base_views


class HomePageView(base_views.TemplateView):
    template_name = 'consultations/home.html'
