from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Custom User Manager to handle user creation
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field must be provided.')
        email = self.normalize_email(email)  # Normalize the email address
        user = self.model(email=email, **extra_fields)  # Create a user instance
        user.set_password(password)  # Set the user's password
        user.save(using=self._db)  # Save the user instance to the database
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # Set is_staff to True for superuser
        extra_fields.setdefault('is_superuser', True)  # Set is_superuser to True

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

# Custom User model that extends AbstractUser
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)  # User's full name
    email = models.EmailField(unique=True, null=True)  # Unique email for each user
    bio = models.TextField(null=True)  # Short biography of the user
    avatar = models.ImageField(null=True, default="avatar.svg")  # User's avatar image

    USERNAME_FIELD = 'email'  # Use email as the username field
    REQUIRED_FIELDS = []  # No additional fields required for user creation

    objects = UserManager()  # Set the custom user manager

    def __str__(self):
        return self.email  # Return the email as the string representation

# Topic model to categorize rooms
class Topic(models.Model):
    name = models.CharField(max_length=200)  # Name of the topic

    def __str__(self):
        return self.name  # Return the topic name as the string representation

# Room model to represent chat rooms
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Room host
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)  # Associated topic
    name = models.CharField(max_length=200)  # Room name
    description = models.TextField(null=True, blank=True)  # Optional room description
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)  # Participants in the room
    updated = models.DateTimeField(auto_now=True)  # Last updated timestamp
    created = models.DateTimeField(auto_now_add=True)  # Created timestamp

    class Meta:
        ordering = ['-updated', '-created']  # Default ordering of rooms

    def __str__(self):
        return self.name  # Return the room name as the string representation

# Message model to represent messages sent in rooms
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who sent the message
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Room where the message was sent
    body = models.TextField()  # Content of the message
    updated = models.DateTimeField(auto_now=True)  # Last updated timestamp
    created = models.DateTimeField(auto_now_add=True)  # Created timestamp

    class Meta:
        ordering = ['-updated', '-created']  # Default ordering of messages

    def __str__(self):
        return self.body[:50]  # Return the first 50 characters of the message body
