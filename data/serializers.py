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

    def save(self): # pylint: disable=arguments-differ
        '''
        save method creates or updates a single db entry
        '''

        # Get or create `DataType` entry first
        data_type, _ = models.DataType.objects.get_or_create(
            name=self.validated_data['dtype']['__str__']
        )

        # Then get or create `Attribute`
        models.Attribute.objects.get_or_create(name=self.validated_data['name'], dtype=data_type)


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

    master_item = serializers.CharField(source='master_item.__str__')
    attribute = AttributeSerializer(many=True)
    measure = MeasureSerializer(many=True)
    link = AMLinkSerializer(many=True)

    class Meta:
        fields = ('__all__')
        model = models.AbstractModel

    def save(self): # pylint: disable=arguments-differ
        '''
        save method creates or updates new db entries
        '''

        # Get or create `Item` entry
        models.Item.objects.get_or_create(name=self.validated_data['master_item']['__str__'])

        # Call `AttributeSerializer with the data to save to new `Attribute` entries
        attribute_serializer = AttributeSerializer(data=self.initial_data['attribute'], many=True)

        # Call `is_valid()` required before we call `save()`
        attribute_serializer.is_valid()
        attribute_serializer.save()
