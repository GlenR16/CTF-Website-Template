from django.db import models
import uuid
import json

class CTF(models.Model):
    name = "Global Variables (Constants)"
    registrations = models.BooleanField(default=True)
    started = models.BooleanField(default=False)
    ended  = models.BooleanField(default=False)
    def total_users(self):
        return User.objects.all().count()
    def total_teams(self):
        return Team.objects.all().count()
    def total_challenges(self):
        return Challenge.objects.all().count()
    def total_solves(self):
        total = 0
        for i in Challenge.objects.all():
            total += i.solves
        return total
    
class Team(models.Model):
    tid = models.CharField(default=uuid.uuid4().hex[:8],primary_key=True,unique=True,max_length=8)
    name = models.CharField(max_length=50)
    score = models.IntegerField(default=0)
    disqualified = models.BooleanField(default=False)
    solved_challenges = models.CharField(max_length=255,blank=True,null=True,default=json.dumps([]))
    def set_solved_challenge(self, cid):
        svc = json.loads(self.solved_challenges)
        svc.append(int(cid))
        self.solved_challenges = json.dumps(svc)
    def get_solved_challenges(self):
        return json.loads(self.solved_challenges)
    def __str__(self):
        return f"{self.name}"
    def members_count(self):
        return len(User.objects.filter(team=self))
    

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
    endpoint = models.CharField(max_length=63,blank=True,null=True)
    points = models.IntegerField()
    solves = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.name}"
    def solved(self):
        self.solves += 1
        if self.points > 20 and self.solves % 5 == 0 :
            self.points-=1
        self.save()