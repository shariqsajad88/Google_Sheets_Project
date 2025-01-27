from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_data_view, name='show_data_view'),
    path('save/', views.save_to_sheet, name='save_to_sheet'),
    path('download/', views.download_db_data, name='download_db_data'),
    path('upload/', views.upload_csv, name='upload_csv'),
]
