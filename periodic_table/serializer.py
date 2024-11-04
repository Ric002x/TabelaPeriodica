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
        lookup_field='symbol'
    )


class ElementDetailSerializer(serializers.ModelSerializer):
    additional_information = serializers.SerializerMethodField()
    physical_properties = serializers.SerializerMethodField()

    class Meta:
        model = Element
        fields = [
            'atomic_number', 'name', 'symbol', 'atomic_mass',
            'electrons_number', 'neutrons_number', 'state_matter',
            'electronic_configuration', 'electron_distribution',
            'ionic_states', 'physical_properties', 'additional_information'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['atomic_mass'] = {
            "value": instance.atomic_mass,
            "unit": "g/mol"
        }
        return representation

    def get_additional_information(self, obj):
        return {
            "description": obj.description,
            "history_and_discovery": obj.history_and_discovery,
            "chemical_properties": obj.chemical_properties,
            "usage": obj.usage,
            "extra_information": obj.extra_information,
        }

    def get_physical_properties(self, obj):
        return {
            "density": {
                "value": obj.density,
                "unit": "g/cm³"
            },
            "melting_point": {
                "Celsius": obj.melting_point,
                "Fahrenheit": obj.melting_point_fahrenheit(),
                "Kelvin": obj.melting_point_kelvin()
            },
            "boiling_point": {
                "Celsius": obj.boiling_point,
                "Fahrenheit": obj.boiling_point_fahrenheit(),
                "Kelvin": obj.boiling_point_kelvin()
            }
        }
