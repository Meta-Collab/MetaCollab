from django.shortcuts import render,redirect
#from .decorators import authenticate_room, authenticate_user
from django.contrib.auth import authenticate, login
from .models import User, Room, RoomToUser
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
import json
import random

# Create your views here.

@api_view(['GET', 'POST'])
#@authenticate_room
def get_room(request, roomuuid):
    roominfo=Room.objects.get(roomuuid=roomuuid)
    context={
        "room" : roominfo,
        "members" : RoomToUser.objects.filter(room=roominfo),

    }
    try:
        url="http://localhost:3000/get_commits"
        response = requests.post(url, json={'room_id': roomuuid})
        response.raise_for_status()
        print("see")
        # return redirect('get_room', roomuuid=room.roomuuid, )
    except:
        print("Error in sending data to Node.js server")
    return render(request,"get_room.html",context)

@csrf_exempt
@api_view(['GET', 'POST'])
def api_list_room(request):
    print("Received a request from the Node.js server")
    commits = request.data.get('commits')
    print(commits)
    return Response('Success!')

@csrf_exempt
@api_view(['GET', 'POST'])
def list_rooms(request):
    print("help")
    user = User.objects.get(id = request.session["user_id"])
    rooms = RoomToUser.objects.filter(user=user)
    print(user)
    if request.method == 'POST':
        #here also make a call to smart contract function
        print("hi")
        ruuid=random.randint(100000000, 9999999999)
        name = request.POST.get('name')
        description = request.POST.get('description')
        room=Room.objects.create(roomuuid=ruuid, name = name, description=description)
        room.save()
        users = request.POST.get('users')
        user_id=request.session['user_id']
        user_id = User.objects.get(id=user_id)
        r = RoomToUser.objects.create(room = room, user = user_id)
        r.save()
        for u in users:
            user_id = User.objects.get(username=u)
            r = RoomToUser.objects.create(room = room, user = user_id)
            r.save()
        users = RoomToUser.objects.filter(room=room)
        user_ids_list = [user.user for user in users]
        accounts = [user.accountNo for user in user_ids_list]
        print(accounts)
        try:
            url="http://localhost:3000/new_room"
            response = requests.post(url, json={'room_id': room.roomuuid, 'members':accounts})
            response.raise_for_status()
            print("see")
            return redirect('get_room', roomuuid=room.roomuuid, )
        except:
            print("Error in sending data to Node.js server")
        return redirect('get_room', roomuuid=room.roomuuid, )
        
    return render(request,"list_rooms.html", {'rooms': rooms})

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
