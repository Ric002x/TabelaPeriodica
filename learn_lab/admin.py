from django.contrib import admin

from .models import Activity, ActivityLevel, ActivityRating, ActivitySubject

# Register your models here.


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'description', 'content',
              'file', 'subject', 'level', 'user', 'is_published']
    search_fields = ['title', 'description']
    list_filter = ['created_at', 'subject', 'level', 'is_published']


@admin.register(ActivitySubject)
class ActivitySubjectAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(ActivityLevel)
class ActivityLevelAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(ActivityRating)
class ActivityRatingAdmin(admin.ModelAdmin):
    fields = ['rating', 'comment', 'created_at', 'updated_at']
    list_display = ['activity', 'user', 'rating', 'created_at', 'updated_at']
