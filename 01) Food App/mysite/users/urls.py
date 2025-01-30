from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'users'


from django.contrib.auth import logout
from django.shortcuts import redirect,render
from django.contrib import messages

def custom_logout(request):
    
    # Get the current username before logging out
    if request.user.is_authenticated:
        user_name = request.user.username
        # Optionally, add a success message with the username
        messages.success(request, f"Goodbye {user_name}, you have been logged out successfully.")
    
        # Log the user out
        logout(request)
        
    # Redirect to a specific page, e.g., the homepage or login page
    return render(request,'users/logout.html')  # Or any other page you'd like to redirect to




urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', views.profilepage, name='profile'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout')

]

