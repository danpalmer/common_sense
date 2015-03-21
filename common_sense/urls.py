from django.conf.urls import patterns, include, url
from django.contrib import admin

from accounts import urls as accounts_urls
from consultations import urls as consultations_urls

urlpatterns = patterns(
    '',

    url(r'^admin/', include(admin.site.urls)),

    url(r'', include(accounts_urls)),
    url(r'', include(consultations_urls)),
)
