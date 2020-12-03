from django.urls import path
from . import views

urlpatterns = [
	path('', views.login),

    path('sign_up', views.sign_up),
    path('create_user', views.create_user),
    path('login', views.log_user),

    path('home', views.home),
]
