from django.urls import path
from . import views

app_name = "scraperapp"
urlpatterns = [
    path('', views.index, name='index'),
    path('scrape/', views.scrape_and_index, name='scrape_and_index'),
]

views.scrape_and_index(None)