from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

# Authentication view for user login
def loginPage(request):
    page_type = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User not found')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    context = {'page': page_type}
    return render(request, 'base/login_register.html', context)

# User logout functionality
def logoutUser(request):
    logout(request)
    return redirect('home')

# User registration view
def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = new_user.username.lower()
            new_user.save()
            login(request, new_user)
            return redirect('home')
        else:
            messages.error(request, 'Registration error occurred')

    return render(request, 'base/login_register.html', {'form': form})

# Home page view with room filtering
def home(request):
    search_query = request.GET.get('q') if request.GET.get('q') else ''

    filtered_rooms = Room.objects.filter(
        Q(topic__name__icontains=search_query) |
        Q(name__icontains=search_query) |
        Q(description__icontains=search_query)
    )

    popular_topics = Topic.objects.all()[:5]
    total_rooms = filtered_rooms.count()
    recent_messages = Message.objects.filter(
        Q(room__topic__name__icontains=search_query))[:3]

    context = {
        'rooms': filtered_rooms,
        'topics': popular_topics,
        'room_count': total_rooms,
        'room_messages': recent_messages
    }
    return render(request, 'base/home.html', context)

# Room detail page view
def room(request, pk):
    selected_room = Room.objects.get(id=pk)
    room_messages = selected_room.message_set.all()
    participants = selected_room.participants.all()

    if request.method == 'POST':
        new_message = Message.objects.create(
            user=request.user,
            room=selected_room,
            body=request.POST.get('body')
        )
        selected_room.participants.add(request.user)
        return redirect('room', pk=selected_room.id)

    context = {
        'room': selected_room,
        'room_messages': room_messages,
        'participants': participants
    }
    return render(request, 'base/room.html', context)

# User profile view
def userProfile(request, pk):
    user_profile = User.objects.get(id=pk)
    user_rooms = user_profile.room_set.all()
    user_messages = user_profile.message_set.all()
    all_topics = Topic.objects.all()
    
    context = {
        'user': user_profile,
        'rooms': user_rooms,
        'room_messages': user_messages,
        'topics': all_topics
    }
    return render(request, 'base/profile.html', context)

# Room creation view
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    all_topics = Topic.objects.all()
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, _ = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': all_topics}
    return render(request, 'base/room_form.html', context)

# Room update view
@login_required(login_url='login')
def updateRoom(request, pk):
    room_to_update = Room.objects.get(id=pk)
    form = RoomForm(instance=room_to_update)
    all_topics = Topic.objects.all()
    
    if request.user != room_to_update.host:
        return HttpResponse('You do not have permission to edit this room.')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, _ = Topic.objects.get_or_create(name=topic_name)
        room_to_update.name = request.POST.get('name')
        room_to_update.topic = topic
        room_to_update.description = request.POST.get('description')
        room_to_update.save()
        return redirect('home')

    context = {'form': form, 'topics': all_topics, 'room': room_to_update}
    return render(request, 'base/room_form.html', context)

# Room deletion view
@login_required(login_url='login')
def deleteRoom(request, pk):
    room_to_delete = Room.objects.get(id=pk)

    if request.user != room_to_delete.host:
        return HttpResponse('You do not have permission to delete this room.')

    if request.method == 'POST':
        room_to_delete.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room_to_delete})

# Message deletion view
@login_required(login_url='login')
def deleteMessage(request, pk):
    message_to_delete = Message.objects.get(id=pk)

    if request.user != message_to_delete.user:
        return HttpResponse('You do not have permission to delete this message.')

    if request.method == 'POST':
        message_to_delete.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message_to_delete})

# User update view
@login_required(login_url='login')
def updateUser(request):
    current_user = request.user
    form = UserForm(instance=current_user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=current_user.id)

    return render(request, 'base/update-user.html', {'form': form})

# Topics page view
def topicsPage(request):
    search_query = request.GET.get('q') if request.GET.get('q') else ''
    filtered_topics = Topic.objects.filter(name__icontains=search_query)
    return render(request, 'base/topics.html', {'topics': filtered_topics})

# Activity page view
def activityPage(request):
    all_room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': all_room_messages})
