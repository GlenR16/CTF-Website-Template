from django.contrib import admin
from django.db.models import Sum
from .models import Team
from .models import User as UserModel
from .models import Challenge as ChallengeModel
from .models import CTF

@admin.register(ChallengeModel)
class Challenge(admin.ModelAdmin):
    list_display = ("name", "solves")
    list_filter = ("category", )

@admin.register(Team)
class Team(admin.ModelAdmin):
    list_display = ("name", "score")
    list_filter = ("disqualified", )
    search_fields = ("tid__startswith", )

@admin.register(UserModel)
class User(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("email__startswith", )

@admin.register(CTF)
class CTF(admin.ModelAdmin):
    list_display = ("name","registrations", "wave1", "wave2", "ended","total_solves","total_users")
    def total_solves(self, obj):
        result = ChallengeModel.objects.aggregate(Sum('solves'))
        return result["solves__sum"]
    def total_users(self, obj):
        result = UserModel.objects.all().count()
        return result

