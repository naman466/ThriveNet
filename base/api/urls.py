from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_api_routes),  # Updated to match new function name
    path('rooms/', views.retrieve_all_rooms),  # Updated to match new function name
    path('rooms/<str:pk>/', views.retrieve_single_room),  # Updated to match new function name
]
