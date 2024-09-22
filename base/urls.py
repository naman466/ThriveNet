from django.urls import path
from . import views

# URL patterns for the application
urlpatterns = [
    # User authentication URLs
    path('login/', views.loginPage, name="login"),  # Login page
    path('logout/', views.logoutUser, name="logout"),  # Logout action
    path('register/', views.registerPage, name="register"),  # Registration page

    # Main application URLs
    path('', views.home, name="home"),  # Home page
    path('room/<str:pk>/', views.room, name="room"),  # Room detail page
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),  # User profile page

    # Room management URLs
    path('create-room/', views.createRoom, name="create-room"),  # Create new room
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),  # Update existing room
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),  # Delete a room
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),  # Delete a message

    # User profile update URL
    path('update-user/', views.updateUser, name="update-user"),  # Update user information

    # Additional pages
    path('topics/', views.topicsPage, name="topics"),  # Topics page
    path('activity/', views.activityPage, name="activity"),  # User activity page
]
