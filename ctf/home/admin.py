from django.contrib import admin
from .models import Team,User,Challenge,CTF
from .models import User as u
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    def email(self,obj):
        return get_object_or_404(u,id=obj.get_decoded().get("_auth_user_id","")).email
    email.short_description = "User Email"
    list_display = ("session_key","email")
    search_fields = ("session_key_startswith",)

@admin.register(Challenge)
class Challenge(admin.ModelAdmin):
    list_display = ("name", "solves","points")
    list_filter = ("category", )

@admin.register(Team)
class Team(admin.ModelAdmin):
    readonly_fields=('tid',)
    list_display = ("name", "score")
    list_filter = ("disqualified", )
    search_fields = ("tid__startswith", )
    fields = ("tid","name","disqualified","score",)

@admin.register(User)
class User(admin.ModelAdmin):
    readonly_fields=('email',"last_login")
    list_display = ("name","email","team")
    search_fields = ("email__startswith", )
    fields = ("email","name","team","is_active","is_staff","is_superuser","user_permissions","groups","last_login")

@admin.register(CTF)
class CTF(admin.ModelAdmin):
    list_display = ("name","registrations", "started", "ended","total_users","total_teams","total_challenges","total_solves")
    

