from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/', views.ReadUser, name='user'),
    path('user/create/', views.CreateUser, name='create_user'),
    path('user/update/<int:id>/', views.UpdateUser, name='update_user'),
    path('user/delete/<int:id>/', views.DeleteUser, name='delete_user'),
]