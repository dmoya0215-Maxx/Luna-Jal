from django.urls import path
from . import views

urlpatterns = [
    path('person/', views.ReadPerson, name='readperson'),
    path('person/create/', views.CreatePerson, name='createperson'),
    path('person/update/<int:id>/', views.UpdatePerson, name='updateperson'),
    path('person/deactivate/<int:id>/', views.DeactivatePerson, name='deactivateperson'),
    path('person/activate/<int:id>/', views.ActivatePerson, name='activateperson'),
]