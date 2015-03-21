from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',

    url(r'^account/profile', views.ProfileEditView.as_view(), name='profile'),
)
