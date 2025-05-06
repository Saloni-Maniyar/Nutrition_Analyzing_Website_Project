# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('analyze/', views.analyze, name='analyze'),
#     path('login/', views.login, name='login'),
#     path('signup/', views.signup, name='signup'),
# ]
"""
URL configuration for Nutrition_Analyzing_Website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('analyze/', views.analyze, name='analyze'),
    path('track/', views.track, name='track'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),  # Registration page
    path('login/', views.login_view, name='login'),      # Login page
    path('logout/', views.logout_view, name='logout'),   # Logout page
    path('save_nutrition/', views.save_nutrition_data, name='save_nutrition_data'), 
    path('fetch_nutrition_data/', views.fetch_nutrition_data, name='fetch_nutrition_data'),
]

