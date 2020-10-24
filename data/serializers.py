'''
Defines serializers used to serialize/deserialize json data to model entries
'''


from rest_framework import serializers

from data import models


class AbstractModelSerializer(serializers.Serializer):
    '''
    Serializer for the `AbstractModel` model
    '''

    class Meta:
        fields = ('__all__')
        model = models.AbstractModel
