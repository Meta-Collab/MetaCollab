from django.shortcuts import redirect
from .models import Room,User
def authenticate_room(view_func):
    def wrapper_func(request, *args, **kwargs):
        roomuuid = kwargs['roomuuid']
        room= Room.objects.get(roomuuid=roomuuid)
        user_id = request.session.get('user_id')
        if user_id is None:
            return redirect('home')
        user=User.objects.get(id=user_id)
        if user not in room.user.all():
            return redirect('error')
        return view_func(request, *args, **kwargs)
    return wrapper_func
