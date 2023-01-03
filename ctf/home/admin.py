from django.contrib import admin
from .models import Team,User,Challenge,CTF
from django.contrib.sessions.models import Session

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    def email(self,obj):
        return obj.get_decoded().get("email", "Not logged in.")
    email.short_description = "Email"
    list_display = ("session_key","email")
    search_fields = ("session_key_startswith",)

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
    

