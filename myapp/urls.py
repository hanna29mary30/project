"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),

    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_changepassword', views.admin_changepassword, name='admin_changepassword'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('admin_home', views.admin_home, name='admin_home'),

    path('admin_book_file_add', views.admin_book_file_add, name='admin_book_file_add'),
    path('admin_book_details_add', views.admin_book_details_add, name='admin_book_details_add'),
    path('admin_book_details_view', views.admin_book_details_view, name='admin_book_details_view'),
    path('admin_book_details_delete', views.admin_book_details_delete, name='admin_book_details_delete'),
    path('admin_book_search', views.admin_book_search, name='admin_book_search'),

    path('admin_user_details_view', views.admin_user_details_view, name='admin_user_details_view'),
    path('admin_user_details_delete', views.admin_user_details_delete, name='admin_user_details_delete'),

    path('admin_train_model', views.admin_train_model, name='admin_train_model'),

    path('user_login', views.user_login_check, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('user_home', views.user_home, name='user_home'),
    path('user_details_add', views.user_details_add, name='user_details_add'),
    path('user_changepassword', views.user_changepassword, name='user_changepassword'),

    path('user_book_search', views.user_book_search, name='user_book_search'),
    path('user_search_view', views.user_search_view, name='user_search_view'),
    path('user_book_search_results', views.user_book_search_results, name='user_book_search_results'),
    path('user_book_ml_results', views.user_book_ml_results, name='user_book_ml_results'),

]
