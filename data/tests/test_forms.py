'''
Tests for `data.models` in the `data` Django web app
'''


import json
import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from data import forms, models


class RetrieveDataFormTests(TestCase):
    '''
    TestCase class for the `RetrieveDataForm` form
    '''

    fixtures = [
        './doc/instanceserializertests.xml'
    ]

    def test_form_raises_error_data_request_not_json(self):
        '''
        `RetrieveDataForm` `.is_valid()` method should raise an error if the data_request data is
        invalid. `data_request` data should be in the form e.g.:

        {
            "UOA": "Film",
            "Book": {...},
            "Person": {...},
            "Review": {...},
            "Country": {...}
        }

        If the data attached to `data_request` field is not json, raise an error
        '''

        # Instantiate the form
        form = forms.RetrieveDataForm({'data_request': 'hello!'})

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        self.assertEqual(
            form.errors['data_request'], ['Expecting value: line 1 column 1 (char 0)']
        )

    def test_form_raises_error_data_request_no_uoa_key(self):
        '''
        `RetrieveDataForm` `.is_valid()` method should raise an error if the data_request data is
        invalid. `data_request` data should be in the form e.g.:

        {
            "UOA": "Film",
            "Book": {...},
            "Person": {...},
            "Review": {...},
            "Country": {...}
        }

        If the data attached to `data_request` field does not contain the "UOA" key, raise an error
        '''

        # Instantiate the form with some valid json, but without "UOA" key
        form = forms.RetrieveDataForm(
            {'data_request': '{"Year": "1", "Age": "2", "Name": "2", "Movie": "3"}'}
        )

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        self.assertEqual(
            form.errors['data_request'], ['Input json doesn''t contain a "UOA" key.'] # pylint: disable=implicit-str-concat
        )

    def test_form_raises_error_data_request_uoa_value_no_item_exists(self):
        '''
        `RetrieveDataForm` `.is_valid()` method should raise an error if the data_request data is
        invalid. `data_request` data should be in the form e.g.:

        {
            "UOA": "Film",
            "Book": {...},
            "Person": {...},
            "Review": {...},
            "Country": {...}
        }

        If the data attached to `data_request` field contains the "UOA" key, but the value
        associated with this key is not a valid `Item` entry, raise an error
        '''

        # Instantiate the form with some valid json, with "UOA" key but an invalid `Item` value
        form = forms.RetrieveDataForm(
            {'data_request': '{"UOA": "Junk"}'}
        )

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        self.assertEqual(
            form.errors['data_request'], ['"Junk" Item does not exist.']
        )

    def test_form_raises_error_data_request_book_value_not_a_dict(self):
        '''
        `RetrieveDataForm` `.is_valid()` method should raise an error if the data_request data is
        invalid. `data_request` data should be in the form e.g.:

        {
            "UOA": "Film",
            "Book": {...},
            "Person": {...},
            "Review": {...},
            "Country": {...}
        }

        If the data attached to `data_request` field contains a valid "UOA" key value pair, but
        the other key value pairs do not have a dictionary in their values, raise an error
        '''

        # Instantiate the form with some valid json, with valid "UOA" key and valid but invalid
        # "Book" value (not a dictionary)
        form = forms.RetrieveDataForm(
            {'data_request': '{"UOA": "Film", "Book": "Junk"}'}
        )

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        self.assertEqual(
            form.errors['data_request'], ['"Book" value is not a dictionary.']
        )

    def test_form_raises_error_data_request_book_value_dict_bad_keys(self):
        '''
        `RetrieveDataForm` `.is_valid()` method should raise an error if the data_request data is
        invalid. `data_request` data should be in the form e.g.:

        {
            "UOA": "Film",
            "Book": {...},
            "Person": {...},
            "Review": {...},
            "Country": {...}
        }

        If the data attached to `data_request` field contains a valid "UOA" key value pair, but
        the other key value pairs do not have a dictionary in their values, raise an error
        '''

        # Instantiate the form with some valid json, with valid "UOA" key and valid but invalid
        # "Book" value (not a dictionary)
        form = forms.RetrieveDataForm(
            {'data_request': '{"UOA": "Film", "Book": {"Junk": "asd", "silly": "2"}}'}
        )

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        self.assertEqual(
            form.errors['data_request'],
            ['"Book" value dictionary doesn''t contain "ATTR", "MEAS" or "LINK" key(s).'] # pylint: disable=implicit-str-concat
        )

    def test_form_is_valid_true_data_request_valid_data(self):
        '''
        `RetrieveDataForm` `.is_valid()` method should return `True` if the submitted data is
        valid. `data_request` data should be in the form e.g.:

        {
            "UOA": "Book",
            "Book": {
                "ATTR": ["title", "category"],
                "MEAS": [],
                "LINK": ["(Book)<-[WRITTEN_BY]-(Person)","(Book)<-[ABOUT]-(Review)"]
            },
            "Person": {
                "ATTR": ["name"],
                "MEAS": ["date_of_birth"],
                "LINK": ["(Person)-[BORN]->(Country)"]
            },
            "Review": {
                "ATTR": [],
                "MEAS": ["AVG(score)"]
            },
            "Country": {
                "ATTR": ["name"]
            }
        }
        '''

        # Create a Book `Item` entry to satisfy code
        models.Item.objects.create(name='Book')

        # Load the data_request json defined at
        # https://www.notion.so/To-do-list-c7fa657a21524f73b91c966e6740b759
        with open(os.path.join(settings.BASE_DIR, 'doc', 'data_request.json')) as f: # pylint: disable=invalid-name
            data_request = json.load(f)

        # Instantiate the form with some valid json, with valid "UOA" key and valid but invalid
        # "Book" value (not a dictionary)
        form = forms.RetrieveDataForm({'data_request': json.dumps(data_request)})

        # Confirm data is valid
        self.assertTrue(form.is_valid())


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

    def test_form_raises_error_abm_match_data_no_abm_entry(self):
        '''
        `UploadCsvFileForm` `.is_valid()` method should raise an error if the abm match data is
        invalid. `abm_match` data should be in the form e.g.:

         {'Year': '1', 'Age': '2', 'Name': '2', 'Movie': '3'}

        If the data references `AbstractModel` ids that do not exist, an error should be raised
        '''

        # Instantiate the form
        form = forms.UploadCsvFileForm(
            {'abm_match_json': '{"Year": "1", "Age": "2", "Name": "2", "Movie": "3"}'},
            self.empty_csv_file
        )

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        # Data loaded by fixtures should contain a single `AbstractModel` entry only with id=1, so
        # the additional references to ids should raise an error
        self.assertEqual(
            form.errors['abm_match_json'],
            ['Data contains references to AbstractModel entries that do not exist.']
        )

    def test_form_raises_error_abm_match_data_csv_column_name_not_found(self):
        '''
        `UploadCsvFileForm` `.is_valid()` method should raise an error if the key strings in the
        `abm_match_json` don't agree with the column names in the input csv.

        If the input csv does not have a column name that is a key in the `abm_match_json`, raise
        error attached to the `upload_file` field
        '''

        # Create an `AbstractModel` entry in the db to use as an id
        abm = models.AbstractModel.objects.create(
            master_item=models.Item.objects.create(name='blah')
        )

        # Open the test file and attach it as an uploaded file
        upload_file = open(
            os.path.join(settings.BASE_DIR, 'doc', 'test_data', 'column_name_error.csv'),
            'rb'
        )

        # Instantiate the form
        form = forms.UploadCsvFileForm(
            {'abm_match_json': json.dumps({'Blah': abm.id})},
            {'upload_file': SimpleUploadedFile(upload_file.name, upload_file.read())}
        )

        # Confirm calling the `.is_valid()` method raises the correct error
        form.is_valid()

        # Uploaded csv does not have a column in it called "blah", so should raise an error
        self.assertEqual(
            form.errors['upload_file'],
            ['Column name "Blah" does not exist in "column_name_error.csv".']
        )

    def test_form_is_valid_true(self):
        '''
        `UploadCsvFileForm` `.is_valid()` method should return `true` if all the input data is
        right.
        '''

        # Create an `AbstractModel` entry in the db to use as an id
        abm = models.AbstractModel.objects.create(
            master_item=models.Item.objects.create(name='blah')
        )

        # Open the test file and attach it as an uploaded file
        upload_file = open(
            os.path.join(settings.BASE_DIR, 'doc', 'test_data', 'column_name_blah.csv'),
            'rb'
        )

        # Instantiate the form
        form = forms.UploadCsvFileForm(
            {'abm_match_json': json.dumps({'Blah': abm.id})},
            {'upload_file': SimpleUploadedFile(upload_file.name, upload_file.read())}
        )

        # Input csv has a column named "Blah" so form should validate this data as
        # `is_valid` == `True`
        self.assertTrue(form.is_valid())

    def test_form_save_creates_instances_is_valid_true(self):
        '''
        `UploadCsvFileForm` `.save()` method should create new `Instance` entries and return them
        if all the input data is right.

        Input data should return `is_valid()` == `True`
        '''

        # Create some valid `AbstractModel` entries
        award = models.AbstractModel.objects.create(
            master_item=models.Item.objects.create(name='award')
        )
        person = models.AbstractModel.objects.create(
            master_item=models.Item.objects.create(name='person')
        )
        film = models.AbstractModel.objects.create(
            master_item=models.Item.objects.create(name='film')
        )

        # Open the test file and attach it as an uploaded file
        upload_file = open(
            os.path.join(settings.BASE_DIR, 'doc', 'test_data', 'oscar_winners.csv'),
            'rb'
        )

        # Instantiate the form
        form = forms.UploadCsvFileForm(
            {'abm_match_json': json.dumps(
                {'Year': award.id, 'Age': person.id, 'Name': person.id, 'Movie': film.id}
            )},
            {'upload_file': SimpleUploadedFile(upload_file.name, upload_file.read())}
        )

        # Input csv has a column named "Blah" so form should validate this data as
        # `is_valid` == `True`
        self.assertTrue(form.is_valid())

    def test_form_save_creates_instances(self):
        '''
        `UploadCsvFileForm` `.save()` method should create new `Instance` entries and return them
        if all the input data is right.

        Data contained within `oscar_winners.csv` should be saved to new `Instance` entries with
        relationships to valid `AbstractModel` entries

        6 entries should be created from this data
        '''

        # Create some valid `AbstractModel` entries
        award = models.AbstractModel.objects.create(
            master_item=models.Item.objects.create(name='award')
        )
        person = models.AbstractModel.objects.create(
            master_item=models.Item.objects.create(name='person')
        )
        film = models.AbstractModel.objects.create(
            master_item=models.Item.objects.create(name='film')
        )

        # Open the test file and attach it as an uploaded file
        upload_file = open(
            os.path.join(settings.BASE_DIR, 'doc', 'test_data', 'oscar_winners.csv'),
            'rb'
        )

        # Instantiate the form
        form = forms.UploadCsvFileForm(
            {'abm_match_json': json.dumps(
                {'Year': award.id, 'Age': person.id, 'Name': person.id, 'Movie': film.id}
            )},
            {'upload_file': SimpleUploadedFile(upload_file.name, upload_file.read())}
        )

        # Call `is_valid()` first then `save()`
        form.is_valid()
        form.save()

        # Confirm 6 `Instance` entries have been created
        self.assertEqual(models.Instance.objects.all().count(), 6)
