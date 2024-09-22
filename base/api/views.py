from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomDetailSerializer  # Updated for consistency
from base.api import serializers


@api_view(['GET'])
def list_api_routes(request):
    available_routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/<id>'
    ]
    return Response(available_routes)


@api_view(['GET'])
def retrieve_all_rooms(request):
    room_list = Room.objects.all()
    serialized_rooms = RoomDetailSerializer(room_list, many=True)
    return Response(serialized_rooms.data)


@api_view(['GET'])
def retrieve_single_room(request, pk):
    try:
        room_instance = Room.objects.get(id=pk)
        serialized_room = RoomDetailSerializer(room_instance, many=False)
        return Response(serialized_room.data)
    except Room.DoesNotExist:
        return Response({"error": "Room not found"}, status=404)
