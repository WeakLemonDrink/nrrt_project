'''
Tests for `data.models` in the `data` Django web app
'''


from django.test import TestCase

from data import models


class DataTypeModelTests(TestCase):
    '''
    TestCase class for the `DataType` model
    '''

    def setUp(self):
        '''
        Common setup for each test definition
        '''

        self.entry = models.DataType.objects.create(name='varchar')

    def test_save_method_sets_name_to_upper(self):
        '''
        `DataType` model entry should save the contents of the `name` field as upper case
        '''

        self.assertEqual(self.entry.name, 'VARCHAR')

    def test_str_method_return_string(self):
        '''
        `DataType` model entry `__str__()` method should return the contents of the `name` field

        e.g. 'VARCHAR'
        '''

        self.assertEqual(str(self.entry), self.entry.name)


class ItemModelTests(TestCase):
    '''
    TestCase class for the `Item` model
    '''

    def setUp(self):
        '''
        Common setup for each test definition
        '''

        self.entry = models.Item.objects.create(name='book')

    def test_save_method_sets_name_to_title(self):
        '''
        `Item` model entry should save the contents of the `name` field as title case
        '''

        self.assertEqual(self.entry.name, 'Book')

    def test_str_method_return_string(self):
        '''
        `Item` model entry `__str__()` method should return the contents of the `name` field

        e.g. 'Book'
        '''

        self.assertEqual(str(self.entry), self.entry.name)
