'''
Defines all views for the `data` django app
'''


from rest_framework import viewsets

from data import models, serializers


class AttributeViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    '''
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for `Attribute` entries
    '''

    model = models.Attribute
    queryset = models.Attribute.objects.all()
    serializer_class = serializers.AttributeSerializer


class MeasureViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    '''
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for `Measure` entries
    '''

    model = models.Measure
    queryset = models.Measure.objects.all()
    serializer_class = serializers.MeasureSerializer


class AMLinkViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    '''
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for `AMLink` entries
    '''

    model = models.AMLink
    queryset = models.AMLink.objects.all()
    serializer_class = serializers.AMLinkSerializer


class AbstractModelViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    '''
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for `AbstractModel` entries
    '''

    model = models.AbstractModel
    queryset = models.AbstractModel.objects.all()
    serializer_class = serializers.AbstractModelSerializer
