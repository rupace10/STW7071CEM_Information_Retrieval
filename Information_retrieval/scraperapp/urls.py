from django.urls import path
from django.shortcuts import redirect
from . import views
import os

app_name = "scraperapp"
urlpatterns = [
    path('', views.index, name='index'),
    path('scrape/', views.scrape_and_index, name='scrape_and_index'),
]

# def check_and_scrape(request):
#     folder_path = '/index/'  # Adjust this path to the folder you want to check
#     if os.path.exists(folder_path):
#         return redirect('scraperapp:index')
#     else:
#         views.scrape_and_index(request)
#         return redirect('scraperapp:index')