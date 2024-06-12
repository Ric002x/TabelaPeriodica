from django.contrib import admin
from .models import Elements

# Register your models here.


@admin.register(Elements)
class ElementsAdmin(admin.ModelAdmin):
    ...