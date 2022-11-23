from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('about', views.about, name="about"),
    path('privacy-policy', views.privacy, name="privacy"),
    path('terms-of-condition', views.terms, name="terms"),
    path('contact', views.contact, name="contact"),
    path('register', views.register, name="register"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('login', views.loginn, name="loginn"),
    path('signout/', views.signout, name="signout"),
    path('forgot-password/', views.forgot_pass, name="forgot_pass"),
    path('change-password/<token>/', views.change_pass, name="change_pass"),
    path('reset-email', views.reset_email, name="reset_email"),
    path('account-confirmation', views.confirmation, name="confirmation"),
    path('radioexample',views.radioexample,name='radioexample'),
    path("radiodesign",views.radiodesign,name='radiodesign'),
    path("radiocode",views.radiocode,name='radiocode'),
    
]