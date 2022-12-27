from django.contrib import admin
from .models import Team
from .models import User
from .models import Challenge
from .models import CTF

@admin.register(Challenge)
class Challenge(admin.ModelAdmin):
    list_display = ("name", "solves")
    list_filter = ("category", )
    #fields = ("name","flag","category","description","hint","endpoint","points")

@admin.register(Team)
class Team(admin.ModelAdmin):
    list_display = ("name", "score")
    list_filter = ("disqualified", )
    search_fields = ("tid__startswith", )
    #fields=("name","disqualified")

@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("email__startswith", )
    #fields = ("name","email","team")

@admin.register(CTF)
class CTF(admin.ModelAdmin):
    list_display = ("name","registrations", "started", "ended","total_users")
    

