'''
Defines forms for the `data` django app
'''


import json
import os

from django import forms
from django.conf import settings

from data import models


class UploadCsvFileForm(forms.Form):
    '''
    Form provides fields for a user to upload a csv file containing instance data, plus extra data
    to describe the file.
    '''

    abm_match_json = forms.CharField(required=True, widget=forms.Textarea)
    upload_file = forms.FileField(required=True, max_length=50, widget=forms.ClearableFileInput())

    def __del__(self):
        '''
        Custom destructor to delete the temporary file if it exists
        '''

        if self.upload_file_path:
            if os.path.exists(self.upload_file_path):
                # Delete the temp file as we're done with it
                os.remove(self.upload_file_path)

    def __init__(self, *args, **kwargs):
        '''
        Override default `__init__()` to store any uploaded files to storage for processing later
        '''

        # Default init
        super().__init__(*args, **kwargs)

        self.upload_file_path = self.save_temporary_file()

    def clean(self):
        '''
        Override form clean to check that:
         * incoming `abm_match_json` json data references valid `AbstractModel` entries
         * incoming `abm_match_json` json data references valid column names in the uploaded csv
           file
        '''

        cleaned_data = super().clean()

        referenced_ids = cleaned_data.get('abm_match_data', None)
        upload_file = cleaned_data.get('upload_file', None)

        # Only do this if we haven't already raised errors!
        if referenced_ids:
            # Check that the referenced `AbstractModel` ids actually exist
            if not all([models.AbstractModel.objects.filter(id=e).exists() for e in referenced_ids.values()]): # pylint: disable=line-too-long
                self.add_error(
                    'abm_match_data',
                    'Data contains references to AbstractModel entries that do not exist.'
                )

        if upload_file:
            # Check the column names in the uploaded csv file
            pass

        return cleaned_data


    def clean_abm_match_json(self):
        '''
        Override field clean to check the abm_match_json is actually json
        '''

        abm_match_json = self.cleaned_data['abm_match_json']

        try:
            _ = json.loads(self.cleaned_data['abm_match_json'])

        except json.JSONDecodeError as err:
            # If input data is not json, raise error
            self.add_error('abm_match_json', err)

        return abm_match_json


    def clean_upload_file(self):
        '''
        Override field clean to check the uploaded file is a valid csv file
        '''

        if not os.path.splitext(self.upload_file_path)[1] == '.csv':
            # If extension is not csv, raise error
            self.add_error(
                'upload_file',
                '"' + os.path.basename(self.upload_file_path) + '" is not a valid csv.'
            )

        return self.cleaned_data.get('upload_file')


    def save_temporary_file(self):
        '''
        Method saves `upload_file` to a temporary location if it exists, and returns the full path
        of the new temporary file. If `upload_file` is not valid, returns None
        '''

        # Return None by default.
        upload_file_path = None

        upload_file = self.files.get('upload_file', None)

        # if uploaded file exists, save to temp location
        if upload_file:
            upload_file_path = os.path.join(settings.TEMP_FILES_DIR, upload_file.name)

            with open(upload_file_path, 'wb+') as destination:
                for chunk in upload_file.chunks():
                    destination.write(chunk)

        return upload_file_path
