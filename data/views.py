'''
Defines all views for the `data` django app
'''


from rest_framework import viewsets

from data import models, serializers


class AbstractModelViewSet(viewsets.ModelViewSet):
    '''
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for `AbstractModel` entries
    '''

    queryset = models.AbstractModel.objects.all()
    serializer_class = serializers.AbstractModelSerializer
