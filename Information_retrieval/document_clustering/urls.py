from django.urls import path
from . import views

app_name = 'document_clustering'

urlpatterns = [
    path('cluster_form/', views.cluster_form_view, name='cluster_form'),
]
