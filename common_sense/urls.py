from allauth import urls as allauth_urls
from django.conf.urls import include, url
from django.contrib import admin

from accounts import urls as accounts_urls
from consultations import urls as consultations_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'', include(accounts_urls, namespace='accounts')),
    url(r'', include(consultations_urls, namespace='consultations')),

    url(r'^accounts/', include(allauth_urls)),
]
