'''
Tests for `data.views` in the `data` Django web app
'''


import json
import os

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from data import serializers


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


class UploadCsvFileViewTests(TestCase):
    '''
    TestCase class for the `UploadCsvFileView` view
    '''

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

    def test_view_post_upload_file_should_be_csv(self):
        '''
        `UploadCsvFileView` view should return a input view following a `get` request

        Response should return 200
        '''
