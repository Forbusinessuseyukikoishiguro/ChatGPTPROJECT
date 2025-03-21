# chatgpt_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('history/', views.history, name='history'),
    path('history/<int:history_id>/', views.history_detail, name='history_detail'),
    path('history/<int:history_id>/delete/', views.delete_history, name='delete_history'),
    path('export/', views.export_history, name='export_history'),
]