from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name = 'financial_planner-home'),
    path('about/', views.about, name = 'financial_planner-about'),
]