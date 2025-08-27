from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # This line adds the 'home' name
    path('recipes/', views.recipes, name='recipes'),  # <-- Add this line
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # <-- Add this line
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('check-username/', views.check_username, name='check_username'),
    path('profile/', views.profile, name='profile'),
]