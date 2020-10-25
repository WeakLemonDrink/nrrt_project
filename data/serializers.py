'''
Defines serializers for the `data` Django app

Serializers defines how a model entry should be serialized to json, and also how input json data
should be validated and saved to a new model entries
'''


from rest_framework import serializers

from data import models


class AttributeSerializer(serializers.ModelSerializer):
    '''
    Serializer for the `Attribute` model
    '''

    attribute_name = serializers.CharField(source='name')
    value_dtype = serializers.CharField(source='dtype.__str__')

    class Meta:
        fields = ['attribute_name', 'value_dtype']
        model = models.Attribute


class MeasureSerializer(serializers.ModelSerializer):
    '''
    Serializer for the `Measure` model
    '''

    measure_name = serializers.CharField(source='name')
    value_dtype = serializers.CharField(source='value_dtype.__str__')

    class Meta:
        fields = ['measure_name', 'measure_type', 'unit_of_measurement', 'value_dtype',
                  'statistic_type', 'measurement_reference_time', 'measurement_precision']
        model = models.Measure


class AMLinkSerializer(serializers.ModelSerializer):
    '''
    Serializer for the `AMLink` model
    '''

    relationship = serializers.CharField(source='relationship.__str__')

    class Meta:
        fields = ['relationship', 'instances_value_dtype', 'time_link', 'link_criteria', 'values']
        model = models.AMLink


class AbstractModelSerializer(serializers.ModelSerializer):
    '''
    Serializer for the `AbstractModel` model
    '''

    attribute = AttributeSerializer(many=True)
    measure = MeasureSerializer(many=True)
    link = AMLinkSerializer(many=True)

    class Meta:
        fields = ('__all__')
        model = models.AbstractModel
