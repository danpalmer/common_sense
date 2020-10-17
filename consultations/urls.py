from django.conf.urls import url

from . import views

app_name= 'consultations'
urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(
        r'^consultations$',
        views.ConsultationsListView.as_view(),
        name='list',
    ),
    url(
        r'^consultations/(?P<pk>\d+)$',
        views.ConsultationView.as_view(),
        name='view',
    )
]
