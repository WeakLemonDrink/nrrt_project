'''
Tests for `data.views` in the `data` Django web app
'''


import json
import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from data import models, serializers


class AbstractModelViewSetTests(TestCase):
    '''
    TestCase class for the `AbstractModelViewSet` drf viewset
    '''

    def setUp(self):
        '''
        Common setup for each test definition
        '''

        # Load the json blob defined at
        # https://github.com/mister-one/onesto/blob/master/ABM/Book
        with open(os.path.join(settings.BASE_DIR, 'doc', 'abm_input.json')) as f: # pylint: disable=invalid-name
            self.json_blob = json.load(f)

    def test_viewset_list_get_method_all(self):
        '''
        `AbstractModelViewSet` viewset `list` view should return all `AbstractModel` entries

        Response should return 200
        '''

        # First deserialize the data using `AbstractModelSerializer` to create the new entries
        serializer = serializers.AbstractModelSerializer(data=self.json_blob)
        serializer.is_valid()
        serializer.save()

        response = self.client.get(reverse('data:abstractmodel-list'))

        # Confirm the response is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_viewset_detail_get_method_returns_ok(self):
        '''
        `AbstractModelViewSet` viewset `retrieve` view should return a single `AbstractModel` entry

        Response should return 200
        '''

        # First deserialize the data using `AbstractModelSerializer` to create the new entries
        serializer = serializers.AbstractModelSerializer(data=self.json_blob)
        serializer.is_valid()
        serializer.save()

        # Serializer should have created new `AbstractModel` entry, pk should be 1
        response = self.client.get(reverse('data:abstractmodel-detail', args=[1]))

        # Confirm the response is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_viewset_create_post_returns_created(self):
        '''
        `AbstractModelViewSet` viewset `create` view should create a single `AbstractModel` entry

        Response should return 201 (created)
        '''

        response = self.client.post(
            reverse('data:abstractmodel-list'), json.dumps(self.json_blob),
            content_type='application/json'
        )

        # Confirm the response is 201 (created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class RetrieveDataViewTests(TestCase):
    '''
    TestCase class for the `RetreiveDataView` view
    '''

    fixtures = [
        './doc/instanceserializertests.xml'
    ]

    def setUp(self):
        '''
        Common setup for each test definition
        '''

        self.request_url = reverse('data:retrieve-data')

    def test_view_get_method_returns_ok(self):
        '''
        `RetreiveDataView` view should return a input view following a `get` request

        Response should return 200
        '''

        response = self.client.get(self.request_url)

        # Confirm the response is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_post_valid_data_request_data(self):
        '''
        `RetreiveDataView` view should return serialized related `Instance` entries if valid
        `data_request` json data is posted
        '''

        # Create a Book `Item` entry to satisfy code
        models.Item.objects.create(name='Book')

        # Load the data_request json defined at
        # https://www.notion.so/To-do-list-c7fa657a21524f73b91c966e6740b759
        with open(os.path.join(settings.BASE_DIR, 'doc', 'data_request.json')) as f: # pylint: disable=invalid-name
            data_request = json.load(f)

        response = self.client.post(self.request_url, {'data_request': data_request})

        # Valid data should return serialized `Instance` data and 200 code to indicate ok
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UploadCsvFileViewTests(TestCase):
    '''
    TestCase class for the `UploadCsvFileView` view
    '''

    fixtures = [
        './doc/test_data/item.xml',
        './doc/test_data/abstractmodel.xml'
    ]

    def setUp(self):
        '''
        Common setup for each test definition
        '''

        self.request_url = reverse('data:upload-csv')

    def test_view_get_method_returns_ok(self):
        '''
        `UploadCsvFileView` view should return a input view following a `get` request

        Response should return 200
        '''

        response = self.client.get(self.request_url)

        # Confirm the response is 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_post_valid_upload_file_and_abm_match_json(self):
        '''
        `UploadCsvFileView` view should create new `Instance` entries following a `post` request
        with valid data

        Response should redirect to the data:upload-csv view on success
        '''

        upload_file = open(
            os.path.join(settings.BASE_DIR, 'doc', 'test_data', 'oscar_winners.csv'), 'rb'
        )

        upload_data = {
            'abm_match_json': '{"Year": "1", "Age": "2", "Name": "2", "Movie": "3"}',
            'upload_file': SimpleUploadedFile(upload_file.name, upload_file.read())
        }

        response = self.client.post(self.request_url, upload_data, follow=True)

        # Successful upload of file should redirect to the `ContractNotice` list view
        self.assertRedirects(response, self.request_url)

    def test_view_post_creates_ranking_clusters(self):
        '''
        `UploadCsvFileView` view should create new `Instance` entries following a `post` request
        with valid data

        `post` method should call `update_ranking_clusters` method to create new `RankingCluster`
        entries related to the new `Instances`
        '''

        upload_file = open(
            os.path.join(settings.BASE_DIR, 'doc', 'test_data', 'oscar_winners.csv'), 'rb'
        )

        upload_data = {
            'abm_match_json': '{"Year": "1", "Age": "2", "Name": "2", "Movie": "3"}',
            'upload_file': SimpleUploadedFile(upload_file.name, upload_file.read())
        }

        self.client.post(self.request_url, upload_data)

        # Successful upload of file should create three new ranking clusters with
        # `ranking_feature` == `NULL`
        self.assertTrue(models.RankingCluster.objects.filter(ranking_feature='NULL').count(), 3)
