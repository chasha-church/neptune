from django.urls import path
from django.conf.urls import include


urlpatterns = [
    path('news/', include('apiv1.news.urls')),
]
