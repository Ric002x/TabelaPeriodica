from django.contrib import admin

from .models import Activity, ActivityLevel, ActivityRating, ActivitySubject

# Register your models here.


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'description', 'content',
              'file', 'thumbnail', 'subject', 'level', 'user', 'is_published']
    search_fields = ['title', 'description']
    list_filter = ['created_at', 'subject', 'level', 'is_published']
    list_display = ['id', 'title', 'user', 'is_published']
    list_editable = ['is_published']


@admin.register(ActivitySubject)
class ActivitySubjectAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['id', 'name']
    list_editable = ['name']


@admin.register(ActivityLevel)
class ActivityLevelAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['id', 'name']


@admin.register(ActivityRating)
class ActivityRatingAdmin(admin.ModelAdmin):
    fields = ['rating', 'comment']
    list_display = ['activity', 'user', 'rating', 'created_at', 'updated_at']
