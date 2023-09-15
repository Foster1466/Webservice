from django.urls import path
from . import views

# URL patterns for our API endpoints, mapping views with URLs.
urlpatterns = [
    path('process', views.processReceipt, name = 'process'),        # URL for processing receipts.
    path('<str:pk>/points', views.getPoints, name = 'retrive'),     # URL for retrieving points by receipt ID.
]