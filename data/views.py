'''
Defines all views for the `data` django app
'''


from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import ContextMixin, View

from rest_framework import viewsets, status

from data import forms, helpers, models, serializers


class AbstractModelViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    '''
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for `AbstractModel` entries
    '''

    model = models.AbstractModel
    queryset = models.AbstractModel.objects.all()
    serializer_class = serializers.AbstractModelSerializer


class AMLinkViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    '''
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for `AMLink` entries
    '''

    model = models.AMLink
    queryset = models.AMLink.objects.all()
    serializer_class = serializers.AMLinkSerializer


class AttributeViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    '''
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for `Attribute` entries
    '''

    model = models.Attribute
    queryset = models.Attribute.objects.all()
    serializer_class = serializers.AttributeSerializer


class InstanceViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    '''
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for `Instance` entries
    '''

    model = models.Instance
    queryset = models.Instance.objects.all()
    serializer_class = serializers.InstanceSerializer


class MeasureViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    '''
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for `Measure` entries
    '''

    model = models.Measure
    queryset = models.Measure.objects.all()
    serializer_class = serializers.MeasureSerializer


class RetrieveDataView(ContextMixin, View):
    '''
    View to return data based on an incoming request
    '''

    form_class = forms.RetrieveDataForm
    template_name = 'data/retrieve_data.html'

    def get(self, request):
        '''
        Renders the new form so user can upload data when get request
        '''

        # Build context ready to pass to render
        context = self.get_context_data(form=self.form_class())

        return render(request, self.template_name, context)

    def post(self, request):
        '''
        Handles post data and returns any related data
        '''

        form = self.form_class(request.POST)

        # If data entered is valid, retrieve `Instance` entries
        if form.is_valid():

            instances_qs = form.retrieve_instances()

            if instances_qs.exists():
                # Serialize queryset and return
                serializer = serializers.InstanceSerializer(instances_qs, many=True)

                return_data = serializer.data
                status_code = status.HTTP_200_OK

            else:
                # If no valid `Instance` queryset, return nothing
                return_data = []
                status_code = status.HTTP_204_NO_CONTENT

            response = JsonResponse(return_data, status_code=status_code)

        else:
            # If not valid, return the form with associated errors
            # Build context ready to pass to render
            context = self.get_context_data(form=form)

            response = render(request, self.template_name, context)

        return response


class UploadCsvFileView(ContextMixin, View):
    '''
    View to handle incoming csvs of instance data.
    '''

    form_class = forms.UploadCsvFileForm
    template_name = 'data/upload_csv.html'

    def get(self, request):
        '''
        Renders the new form so user can upload data when get request
        '''

        # Build context ready to pass to render
        context = self.get_context_data(form=self.form_class())

        return render(request, self.template_name, context)

    def post(self, request):
        '''
        Handles post data and returns any created `Instance` entries
        when successful
        '''

        form = self.form_class(request.POST, request.FILES)

        # If data entered is valid, call `form.save()` to create new entries
        if form.is_valid():

            new_entries = form.save()

            # Get the unique `Item` entries out of the returned instances
            item_qs = models.Item.objects.filter(
                id__in=[e.abm.master_item.id for e in new_entries]
            )

            # Update `RankingCluster` entries with ranking_features=NULL
            helpers.update_ranking_clusters(item_qs)

            # Create the success message
            messages.add_message(
                request,
                messages.SUCCESS,
                '{!s} new Instance entries added to the database successfully.'.format(
                    len(new_entries)
                )
            )

            # Redirect to a view showing success
            response = HttpResponseRedirect(reverse('data:upload-csv'))

        else:
            # If not valid, return the form with associated errors
            # Build context ready to pass to render
            context = self.get_context_data(form=form)

            response = render(request, self.template_name, context)

        return response
