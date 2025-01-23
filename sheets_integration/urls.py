from django.urls import path
from . import views

urlpatterns = [
    path('fetch/', views.fetch_from_sheet, name='fetch_from_sheet'),
    path('save/', views.save_to_sheet, name='save_to_sheet'),

]