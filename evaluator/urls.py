from django.urls import path
from . import views

app_name = 'evaluator'

urlpatterns = [
    path('', views.home, name='home'),
    path('simple/', views.evaluate_simple, name='simple'),
    path('descriptive/', views.evaluate_descriptive, name='descriptive'),
    path('report/<int:pk>/', views.view_report, name='view_report'),
    path('download/<int:pk>/', views.download_report, name='download_report'),
    path('list/', views.evaluation_list, name='list'),
]
