from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User

# Custom user creation form to register a new user
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # Specify the user model
        fields = ['name', 'username', 'email', 'password1', 'password2']  # Fields to include in the form

# Form for creating and updating Room instances
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room  # Specify the Room model
        fields = '__all__'  # Include all fields
        exclude = ['host', 'participants']  # Exclude these fields from the form

# Form for updating user information
class UserForm(forms.ModelForm):
    class Meta:
        model = User  # Specify the User model
        fields = ['avatar', 'name', 'username', 'email', 'bio']  # Fields to be included
