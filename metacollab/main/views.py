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
from django.http import HttpRequest
import json
import random

#from fl.client import main
# Create your views here.


#@authenticate_room
@csrf_exempt
@api_view(['GET', 'POST'])
def get_room(request, roomuuid):
    roominfo=Room.objects.get(roomuuid=roomuuid)
    context={
        "room" : roominfo,
        "members" : RoomToUser.objects.filter(room=roominfo),
        "roomuuid":roomuuid,

    }
    if request.method=='POST' :
        #federated_learning(request._request)
        print(request.POST.get('action'))
        if request.POST.get('action') == 'train':
            try:
                # print("done3")
                # received_url = 'https://gateway.pinata.cloud/ipfs/QmUTsRiseFSv76FSrVVuFEhZbpeQZ9wizB696vpYxRHxma' #data['url']
                # roominfo.url=received_url
                # roominfo.save()
                print("done")
                url="http://localhost:3000/upload_file"
                response = requests.post(url, json={'file_path':'/home/nandika/MetaCollab/metacollab/fl/saved_models/mobilenetv2/fingerprint.pb', 'room_id':roomuuid})
                response.raise_for_status()
                print("see")
                data = response.json()
                # url = 'https://gateway.pinata.cloud/ipfs/QmUTsRiseFSv76FSrVVuFEhZbpeQZ9wizB696vpYxRHxma' #data['url']
                url=data['url']
                cid = data['cid']
                roominfo.url=url
                roominfo.cid=cid
                roominfo.save()
                print(url,cid)
                

            except:
                print("Error in sending data to Node.js server")
        if request.POST.get('action') == 'submit':
            try:
                updated_string=request.GET.get('string')
                # Write the updated string to the file
                # put string in gfg.txt path
                with open('gfg.txt', 'w') as file:
                    file.write(updated_string)
                from fl.client import main
                main(1)
                # #get string from gfg.txt
                with open('/home/nandika/MetaCollab/metacollab/fl/gfg.txt', 'r') as file:
                # Read the entire contents of the file into a string
                   complete_string = file.read()
                put_string(updated_string,roomuuid)
                #return string and put string in blockchain
            except:
                print("error")

    return render(request,"get_room.html",context)

# @csrf_exempt
# @api_view(['GET', 'POST'])
# def api_list_room(request):
#     print("Received a request from the Node.js server")
#     commits = request.data.get('commits')
#     print(commits)
#     #return Response('Success!')
#     return render(request,'get_commits.html',{'commmits':commits})

@csrf_exempt
@api_view(['GET', 'POST'])
def list_rooms(request):
    print("help")
    user = User.objects.get(id = request.session["user_id"])
    print(request.session["user_id"])
    rooms = RoomToUser.objects.filter(user=user)
    print(rooms)
    print(user)
    if request.method == 'POST':
        #here also make a call to smart contract function
        print("hi")
        ruuid=random.randint(100000000, 9999999999)
        name = request.POST.get('name')
        description = request.POST.get('description')
        print("room_uuid",ruuid)
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
    accountNo='0xe2ba10c388ef4a013db4ff13f56b742893208d05'

    # put_string("hi",1548133828)
    #get_commits(1548133828)
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
def federated_learning(request):
    #file='/files/hello.pkl'
    #run main in server.py
    from fl.client import main
    main(1)
    file_path='fl/saved_models/mobilenetv2/saved_models.pb'
    try:
        url="http://localhost:3000/take_file"
        response = requests.post(url, json={'file_path': file_path})
        response.raise_for_status()
        data = response.json()
        received_url = data['url']
        print(url)
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
        # put string in gfg.txt path
        with open('gfg.txt', 'w') as file:
            file.write(updated_string)
        from fl.client import main
        main(1)
        # #get string from gfg.txt
        with open('gfg.txt', 'r') as file:
        # # Read the entire contents of the file into a string
            complete_string = file.read()
        put_string(complete_string,roomuuid)
        #return string and put string in blockchain
        
    return render(request, "update_model.html")

def get_commits(request,roomuuid):
    commits={}
    
    url="http://localhost:3000/get_commits"
    response = requests.post(url, json={'room_id': roomuuid})
    response.raise_for_status()
    data = response.json()
    print(data)
    #commits='[ 7.81871229e-02 -4.58515435e-01 -7.39910543e-01 -1.21237881e-01 1.18119540e-02  2.05976233e-01 -7.21554339e-01 -6.48166612e-02 8.36113170e-02  5.00397974e-22 -6.65314180e-22 -8.04441097e-23 -2.41206422e-01  1.55485459e-02 -1.80058792e-01 -5.77486038e-01 2.82645345e-01 -2.47149408e-01 -1.29563004e-01 -5.72289377e-02 -1.34234670e-23  1.42827420e-03  6.42313480e-01 -8.67906958e-02 -6.00320927e-04  2.15270277e-03  4.66955379e-02  3.41252493e-22 3.20650823e-03 -7.62496144e-02 -3.43744314e-21  5.17112970e-21 ]'
    # Retrieve 'commits' from the response
    commits = data.get('commits', [])
    #commits = data['commits']
    #int(commits)


    # print("Error in sending data to Node.js server")
    print(commits)
    return render(request,'get_commits.html',{'commits':commits})

def upload_file(file_path,room_id):
    try:
        url="http://localhost:3000/get_commits"
        response = requests.post(url, json={'room_id': room_id})
        response.raise_for_status()
        data = response.json()
        #commits = data['commits']
        print(data)
        
    except:
        print("Error in sending data to Node.js server")

def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully: {filename}")
    else:
        print(f"Failed to download file from {url}")