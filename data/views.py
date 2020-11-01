'''
Defines all views for the `data` django app
'''


from django.shortcuts import render
from django.views.generic.base import ContextMixin, View

from rest_framework import viewsets

from data import forms, models, serializers


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


class MeasureViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    '''
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for `Measure` entries
    '''

    model = models.Measure
    queryset = models.Measure.objects.all()
    serializer_class = serializers.MeasureSerializer


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

    # def post(self, request, *args, **kwargs):
    #     '''
    #     Handles post data and returns a created `ContractNotice` or `ContractAwardNotice` data
    #     when successful
    #     '''

    #     form = self.form_class(request.POST, request.FILES)

    #     # If data entered is valid, call `form.save()` to create new entries
    #     if form.is_valid():

    #         new_entry = form.save()

    #         # Create the success message
    #         messages.add_message(
    #             request,
    #             messages.SUCCESS,
    #             '{} {} was added to the database successfully.'.format(
    #                 new_entry._meta.verbose_name, new_entry
    #             )
    #         )

    #         # Redirect to a view showing success
    #         response = HttpResponseRedirect(
    #             reverse('tenders:{}-list'.format(new_entry._meta.model_name))
    #         )

    #     else:
    #         # If not valid, return the form with associated errors
    #         # Build context ready to pass to render
    #         context = self.get_context_data(form=form)

    #         response = render(request, self.template_name, context)

    #     return response
