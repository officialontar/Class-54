from django.urls import path
from . import views
from django.contrib.auth import views as auth_views   # ✅ এটা যোগ করতে হবে

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name="profile"),
    path('edit-recruiter-profile/', views.edit_recruiter_profile, name="edit_recruiter_profile"),

    path('change-password/', views.change_password, name='change_password'),
]