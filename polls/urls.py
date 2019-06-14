from django.urls import path

from . import views

urlpatterns = [
    path('current_temperature/', views.get_avg_temperature, name='get_avg_temperature'),
]