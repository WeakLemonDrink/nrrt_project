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


class RelationshipModelTests(TestCase):
    '''
    TestCase class for the `Relationship` model
    '''

    def setUp(self):
        '''
        Common setup for each test definition
        '''

        self.entry = models.Relationship.objects.create(
            relationship_str='(Book)<-[WROTE]-(Person)'
        )

    def test_save_method_creates_book_item(self):
        '''
        `Relationship` save method should use strings in the input `relationship_str` to create
        new `Item` entries that can be linked via a `ManyToMany` relationship field

        The input `relationship_str` e.g. (Book)<-[WROTE]-(Person) contains `Item` entries in
        between the brackets
        '''

        # Confirm that the creation of `self.entry` has also created a new `Book` `Item` entry
        self.assertTrue(models.Item.objects.filter(name='Book').exists())

    def test_save_method_creates_person_item(self):
        '''
        `Relationship` save method should use strings in the input `relationship_str` to create
        new `Item` entries that can be linked via a `ManyToMany` relationship field

        The input `relationship_str` e.g. (Book)<-[WROTE]-(Person) contains `Item` entries in
        between the brackets
        '''

        # Confirm that the creation of `self.entry` has also created a new `Person` `Item` entry
        self.assertTrue(models.Item.objects.filter(name='Person').exists())

    def test_save_method_links_book_person_items_to_entry(self):
        '''
        `Relationship` save method should use strings in the input `relationship_str` to create
        new `Item` entries that can be linked via a `ManyToMany` relationship field

        Two new `Item` entries should be linked to the new `Relationship` entry via a `ManyToMany`
        field
        '''

        self.assertEqual(self.entry.item.all().count(), 2)
