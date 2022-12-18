from django.db import models
import uuid

class CTF(models.Model):
    name = "Global Variables (Constants)"
    registrations = models.BooleanField(default=True)
    wave1 = models.BooleanField(default=False)
    wave2 = models.BooleanField(default=False)
    ended  = models.BooleanField(default=False)
    
class Team(models.Model):
    tid = models.CharField(default=uuid.uuid4().hex[:8],primary_key=True,unique=True,max_length=8)
    name = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
    disqualified = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name}"

class User(models.Model):
    uid = models.AutoField(primary_key=True,unique=True)
    name = models.CharField(max_length=50)
    email = models.CharField(unique=True,max_length=50)
    password = models.CharField(max_length=50)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL,blank=True,null=True)
    def __str__(self):
        return f"{self.name}"

class Challenge(models.Model):
    cid = models.AutoField(primary_key=True,unique=True)
    name = models.CharField(max_length=50)
    flag = models.CharField(max_length=63)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=511)
    hint = models.CharField(max_length=127,blank=True,null=True)
    endpoint = models.CharField(max_length=63)
    points = models.IntegerField()
    solves = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.name}"
    def solved():
        self.solves += 1
        if self.points > 20 and self.solves % 5 == 0 :
            self.points-=1