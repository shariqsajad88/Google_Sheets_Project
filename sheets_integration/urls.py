from django.urls import path
from . import views

urlpatterns = [
    path('fetch/', views.fetch_from_sheet, name='fetch_from_sheet'),


]