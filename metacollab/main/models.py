from django.db import models

# Create your models here.
class User(models.Model):
    accountNo= models.CharField(max_length=100,unique=True)
    username= models.UUIDField(unique=True)
    def __str__(self):
        return str(self.username)

class Room(models.Model):
    roomuuid= models.IntegerField(unique=True)
    name=models.CharField(max_length=255)
    description=models.TextField()
    cid=models.CharField(max_length=255,default=None, null=True, blank=True)
    url=models.CharField(max_length=255,default=None, null=True, blank=True)
    def __str__(self):
        return str(self.roomuuid)

class RoomToUser(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)





