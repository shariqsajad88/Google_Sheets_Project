from django.urls import path
from . import views

urlpatterns = [
    path('', views.fetch_from_sheet, name='fetch_from_sheet'),
    path('save/', views.save_to_sheet, name='save_to_sheet'),
    path('download/', views.download_sheet, name='download_sheet'),
    path('upload/', views.upload_csv, name='upload_csv'),
]
