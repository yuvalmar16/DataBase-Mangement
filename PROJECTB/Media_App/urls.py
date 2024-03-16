from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='index'),
   path('Rankings.html', views.Rankings, name='Rankings'),
   path('Query_Results.html', views.Query_Results, name='Query_Results'),
   path('Records_Management.html', views.Records_Management, name='Records_Management'),

]
