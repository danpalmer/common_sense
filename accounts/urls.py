from django.conf.urls import url

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^accounts/profile', views.ProfileEditView.as_view(), name='profile'),
]
