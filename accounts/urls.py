from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',

    url(r'^account/profile', views.TopicEditView.as_view()),
)
