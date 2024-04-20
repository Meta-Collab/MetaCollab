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

#from fl.client import main
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
    if request.method=='POST':
        federated_learning()

    return render(request,"get_room.html",context)

@csrf_exempt
@api_view(['GET', 'POST'])
def api_list_room(request):
    print("Received a request from the Node.js server")
    commits = request.data.get('commits')
    print(commits)
    #return Response('Success!')
    return render(request,'get_commits.html',{'commmits':commits})

@csrf_exempt
@api_view(['GET', 'POST'])
def list_rooms(request):
    print("help")
    user = request.user
    rooms = [Room.objects.get(id=1), Room.objects.get(id=2)]
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

@api_view(['GET', 'POST'])
def federated_learning():
    #file='/files/hello.pkl'
    #run main in server.py
    from fl.client import main
    main(1)
    file_path='fl/saved_models/mobilenetv2/saved_models.pb'
    try:
        url="http://localhost:3000/take_file"
        response = requests.post(url, json={'file_path': file_path})
        response.raise_for_status()
        print("see")
        
    except:
        print("Error in sending data to Node.js server")
    #save in ipfs


def save_ipfs_cid(request):
    cid = request.data.get('cid')
    room_id = request.data.get('room_id')
    room=Room.objects.get(roomuuid=room_id)
    room.cid=cid
    room.save()
    return Response({"message": "Success"}, status=200)

    
def put_string(complete_string,roomuuid):
    try:
        url="http://localhost:3000/put_string"
        response = requests.post(url, json={'complete_string': complete_string,"roomuuid":roomuuid})
        response.raise_for_status()
        print("see")
        
    except:
        print("Error in sending data to Node.js server")


def update_model(request,roomuuid):
    if request.method == 'POST':
        #get file from blockchain
        #file=fl/saved_models/mobilenetv2/saved_model.pb

        updated_string=request.GET.get('string')
        # Write the updated string to the file
        #put string in gfg.txt path
        # with open('gfg.txt', 'w') as file:
        #     file.write(updated_string)
        from fl.client import main
        main(1)
        # #get string from gfg.txt
        with open('gfg.txt', 'r') as file:
        # # Read the entire contents of the file into a string
            complete_string = file.read()
        put_string(complete_string,roomuuid)
        #return string and put string in blockchain
        
    return render(request, "update_model.html")

def get_commits(request,room_id):
    try:
        url="http://localhost:3000/get_commits"
        response = requests.post(url, json={'room_id': room_id})
        response.raise_for_status()
        print("see")
        
    except:
        print("Error in sending data to Node.js server")
    return render(request,'get_commits.html')