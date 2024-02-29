"""Admin wiev modification"""

from django.contrib import admin
from .models import Profession, Skill, Topic


class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'description')


class SkillAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'description')


class TopicAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'description')


admin.site.register(Profession, ProfessionAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Topic, ProfessionAdmin)
