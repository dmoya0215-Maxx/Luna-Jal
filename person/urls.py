from django.urls import path
from . import views

urlpatterns = [
    path('person/', views.ReadPerson, name='readperson'),
    path('person/create/', views.CreatePerson, name='createperson'),
    path('person/update/<int:id>/', views.UpdatePerson, name='updateperson'),
    path('person/delete/<int:id>/', views.DeletePerson, name='deleteperson'),
]