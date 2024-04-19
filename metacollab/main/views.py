from django.shortcuts import render,redirect
from .decorators import authenticate_room, authenticate_user
from django.contrib.auth import authenticate, login
from .models import User, Room, RoomToUser
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@api_view(['GET', 'POST'])
@authenticate_room
def get_room(request,roomuuid):
    roominfo=Room.objects.get(roomuuid=roomuuid)
    context={
        "room" : roominfo,
        "members" : RoomToUser.objects.filter(room=roominfo)
    }
    return render(request,"get_room.html",context)

@csrf_exempt
@api_view(['GET', 'POST'])
def api_list_room(request):
    print("Received a request from the Node.js server")
    myString = request.data.get('myString')
    print(myString)
    return Response('Success!')

@csrf_exempt
@api_view(['GET', 'POST'])
def list_room(request):
    user = User.objects.get(id = request.session["user_id"])
    rooms = RoomToUser.objects.filter(user=user)

    if request.method == 'POST':
        #here also make a call to smart contract function
        ruuid=uuid.uuid4()
        name = request.POST.get('name')
        description = request.POST.get('description')
        room=Room.objects.create(roomuuid=ruuid, name = name, description=description)
        room.save()
        users = request.POST.get('users')
        for u in users:
            user_id = User.objects.get(username=u)
            r = RoomToUser.objects.create(room = room, user = user_id)
            r.save()
        return redirect('get_room', roomuuid=room.roomuuid)
        
    return render(request,"list_rooms.html", {'room': rooms})

@api_view(['GET', 'POST'])
def home(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            metamask_account = data.get('user_id')
            user = User.objects.get(accountNo = metamask_account)
            if user is None:
                user = User.objects.create(accountNo = metamask_account, username = uuid.uuid4())
                user.save()
            request.session['user_id'] = user.id
        except json.JSONDecodeError as e:
            print(e)
    return render(request, "home.html")
