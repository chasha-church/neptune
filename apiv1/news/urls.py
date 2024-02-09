from django.urls import path

from apiv1.news import views

urlpatterns = [
    path('', views.NewsList.as_view(), name='news_list'),
    path('<int:pk>/', views.NewsDetails.as_view(), name='news_details'),
]
