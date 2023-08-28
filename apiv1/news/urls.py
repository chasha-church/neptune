from django.urls import path

from apiv1.news import views

urlpatterns = [
    path('', views.NewsList.as_view(), name='news_list'),
]
