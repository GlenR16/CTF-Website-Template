from django.db import models
import uuid

# Create your models here.
class Team(models.Model):
    tid = models.CharField(default=uuid.uuid4().hex[:8],primary_key=True,unique=True,max_length=8)
    name = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
    disqualified = models.BooleanField(default=False)

class User(models.Model):
    uid = models.AutoField(primary_key=True,unique=True)
    name = models.CharField(max_length=50)
    email = models.CharField(unique=True,max_length=50)
    password = models.CharField(max_length=50)
    uscore = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL,blank=True,null=True)

class Challenge(models.Model):
    cid = models.AutoField(primary_key=True,unique=True)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    points = models.IntegerField()
    solves = models.IntegerField(default=0)

    def solved():
        self.solves += 1
        if self.points > 20 and self.solves % 5 == 0 :
            self.points-=1