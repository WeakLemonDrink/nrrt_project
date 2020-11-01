'''
Tests for `data.models` in the `data` Django web app
'''


import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from data import forms


class UploadCsvFileFormTests(TestCase):
    '''
    TestCase class for the `UploadCsvFileForm` form
    '''

    def setUp(self):
        '''
        Common setup for use across the test methods
        '''

        # request.POST data needs to be an empty dictionary to satisfy the form structure
        self.post_data = {}

        # Create some empty file to test raising errors
        self.empty_csv_file = {'upload_file': SimpleUploadedFile('instances.csv', bytes(2))}

    def test_form_init_saves_upload_file_to_tmp(self):
        '''
        `UploadCsvFileForm` `__init__()` method should save a xml file in `request.FILES` to a
        temporary location for use in `.clean()` and `.save()` methods

        `__init__()` method should save the file to a path defined by `settings.TEMP_FILES_DIR`
        and the file name, and store the path to `upload_file_path`
        '''

        # Instantiate the form
        form = forms.UploadCsvFileForm(self.post_data, self.empty_csv_file)

        # Confirm the file has been saved to the `settings.TEMP_FILES_DIR` location
        self.assertTrue(os.path.isfile(form.upload_file_path))

    def test_form_del_removes_file_from_temp(self):
        '''
        `UploadCsvFileForm` `__del__()` method should remove a file saved to the `upload_file_path`
        location when the class instance is destroyed
        '''

        # Instantiate the form
        form = forms.UploadCsvFileForm(self.post_data, self.empty_csv_file)

        upload_file_path = form.upload_file_path

        # Delete the form, which should call the `__del__()` method
        del form

        # Confirm the file has been removed from the `upload_file_path` location
        self.assertFalse(os.path.isfile(upload_file_path))

    def test_form_raises_error_upload_file_not_csv(self):
        '''
        `UploadCsvFileForm` `.is_valid()` method should raise an error if the uploaded file is
        invalid

        If the file does not have a .csv extension, an error should be raised attached to the
        `upload_file` field
        '''

        file_name = 'instances.xml'

        form = forms.UploadCsvFileForm(
            self.post_data, {'upload_file': SimpleUploadedFile(file_name, bytes(2))}
        )

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        self.assertEqual(
            form.errors['upload_file'], ['"' + file_name + '" is not a valid csv.']
        )

    def test_form_raises_error_abm_match_data_not_json(self):
        '''
        `UploadCsvFileForm` `.is_valid()` method should raise an error if the abm match data is
        invalid. `abm_match` data should be in the form e.g.:

         {'Year': '1', 'Age': '2', 'Name': '2', 'Movie': '3'}

        If the data attached to `abm_match` field is not json, raise an error
        '''

        # Instantiate the form
        form = forms.UploadCsvFileForm({'abm_match_json': 'hello!'}, self.empty_csv_file)

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        self.assertEqual(
            form.errors['abm_match_json'], ['Expecting value: line 1 column 1 (char 0)']
        )
