from django.contrib import admin
from table_elements.models import Elements

# Register your models here.


@admin.register(Elements)
class ElementsAdmin(admin.ModelAdmin):
    list_display = ['name', 'atomic_number', 'symbol']
    list_per_page = 30
    ordering = 'id',
    search_fields = 'name',
    prepopulated_fields = {
        'slug': ('name',)
    }
