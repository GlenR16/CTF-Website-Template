from django.contrib import admin
from .models import Team
from .models import User
from .models import Challenge
from .models import CTF

@admin.register(Challenge)
class Challenge(admin.ModelAdmin):
    list_display = ("name", "solves","points")
    list_filter = ("category", )

@admin.register(Team)
class Team(admin.ModelAdmin):
    list_display = ("name", "score")
    list_filter = ("disqualified", )
    search_fields = ("tid__startswith", )
    fields=("tid","name","disqualified")

@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ("name","email","team")
    search_fields = ("email__startswith", )
    fields = ("name","email","team")

@admin.register(CTF)
class CTF(admin.ModelAdmin):
    list_display = ("name","registrations", "started", "ended","total_users","total_teams","total_challenges","total_solves")
    

