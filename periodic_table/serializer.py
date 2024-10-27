from rest_framework import serializers

from .models import Element


class ElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = [
            'atomic_number', 'element_link', 'name', 'symbol', 'atomic_mass'
        ]

    element_link = serializers.HyperlinkedIdentityField(
        view_name="periodic_table:api_elements_detail_view",
        lookup_field='slug'
    )


class ElementDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = [
            'atomic_number', 'name', 'symbol', 'atomic_mass',
            'description', 'electrons_number', 'neutrons_number', 'density',
            'melting_point', 'boiling_point', 'state_matter',
            'electronic_configuration', 'electron_distribution',
            'ionic_states'
        ]
