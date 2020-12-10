from django.urls import path
from . import views

urlpatterns = [
	path('', views.login),

    path('sign_up', views.sign_up),
    path('create_user', views.create_user),
    path('login', views.log_user),
    path('logout', views.login),

    path('home', views.home),
    path('why_this_matters', views.why),
    path('totals', views.totals),
    path('add', views.add_action_page),

    path('process_action', views.process_action),

    path('profile/<int:id>', views.profile),
]
