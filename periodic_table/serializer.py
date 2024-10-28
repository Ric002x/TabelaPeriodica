from rest_framework import serializers

from .models import Element


class ElementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = [
            'atomic_number', 'element_link', 'name', 'symbol', 'atomic_mass',
            'state_matter', 'electronic_configuration'
        ]

    element_link = serializers.HyperlinkedIdentityField(
        view_name="periodic_table:api_elements_detail_view",
        lookup_field='slug'
    )


class ElementDetailSerializer(serializers.ModelSerializer):
    melting_point = serializers.SerializerMethodField()
    boiling_point = serializers.SerializerMethodField()

    class Meta:
        model = Element
        fields = [
            'atomic_number', 'name', 'symbol', 'atomic_mass',
            'electrons_number', 'neutrons_number', 'density',
            'melting_point', 'boiling_point', 'state_matter',
            'electronic_configuration', 'electron_distribution',
            'ionic_states'
        ]

    def get_melting_point(self, obj):
        return {
            "Celcius": obj.melting_point,
            "Fahrenheit": obj.melting_point_fahrenheit(),
            "Kelvin": obj.melting_point_kelvin()
        }

    def get_boiling_point(self, obj):
        return {
            "Celcius": obj.boiling_point,
            "Fahrenheit": obj.boiling_point_fahrenheit(),
            "Kelvin": obj.boiling_point_kelvin()
        }
