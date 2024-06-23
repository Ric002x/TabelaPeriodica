from django.contrib import admin
from .models import Activity, ActivityLevel, ActivitySubject

# Register your models here.


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    fields = ['title', 'user', 'category', 'level']
    search_fields = ['title', 'description']
    list_filter = ['created_at', 'subject', 'level']


@admin.register(ActivitySubject)
class ActivitySubjectAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(ActivityLevel)
class ActivityLevelAdmin(admin.ModelAdmin):
    fields = ['name']
