from django.urls import path
from . import views

urlpatterns=[
   path('', views.index, name='index'),
   path('Add_a_Movie.html/', views.add_movie, name='Add_a_Movie'),
   path('Query_Results.html/', views.Query_Results, name='Query_Results'),
]
