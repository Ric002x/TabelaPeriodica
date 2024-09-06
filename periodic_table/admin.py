from django.contrib import admin

from periodic_table.models import Element

# Register your models here.


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    fields = ['name', 'slug', 'symbol', 'description', 'cover_image',
              'bohr_model', 'atomic_number', 'atomic_mass',
              'electrons_number', 'neutrons_number', 'density',
              'melting_point', 'boiling_point', 'state_matter',
              'electronic_configuration', 'electron_distribution',
              'ionic_states', 'history_and_discovery',
              'chemical_properties', 'usage', 'extra_information']
    list_display = ['name', 'atomic_number', 'symbol']
    list_per_page = 30
    ordering = 'id',
    search_fields = 'name',
    prepopulated_fields = {
        'slug': ('name',)
    }
