from django.contrib import admin
from django.urls import path, include
from RTAwebsite import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home, name='home'),

    path('register', views.register, name='register'), 
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),

    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('aiModels', views.aiModels, name='aiModels'),
    path('contact', views.contact, name='contact'),
    path('userAccount', views.userAccount, name='userAccount'),
    path('conversion', views.conversion, name='conversion'),
]
