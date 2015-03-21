from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',

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
)
