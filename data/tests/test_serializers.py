'''
Tests for `data.serializers` in the `data` Django web app
'''


import json
import os

from django.conf import settings
from django.test import TestCase

from data import models, serializers


class AttributeSerializerTests(TestCase):
    '''
    TestCase class for the `AttributeSerializer` serializer
    '''

    def setUp(self):
        '''
        Common setup for each test definition
        '''

        self.json_blob = {
            'attribute_name': 'title',
            'value_dtype': 'VARCHAR'
        }

    def test_serializer_serializes_correctly(self):
        '''
        `AttributeSerializer` should serialize an input `Attribute` entry to json in a format that
        agrees with the format defined at
        https://github.com/mister-one/onesto/blob/master/ABM/Book
        '''

        # Create an `Attribute` entry
        dtype_vchar = models.DataType.objects.create(name='varchar')
        attribute = models.Attribute.objects.create(name='title', dtype=dtype_vchar)

        serializer = serializers.AttributeSerializer(attribute)

        self.assertEqual(serializer.data, self.json_blob)

    def test_serializer_validates_data_correctly(self):
        '''
        `AttributeSerializer` should validate input json blob data as valid

        We need to call the `is_valid()` method before saving the data to new model entries
        '''

        serializer = serializers.AttributeSerializer(data=self.json_blob)

        self.assertTrue(serializer.is_valid())

    def test_serializer_deserializes_data_correctly_creates_data_type(self):
        '''
        `AttributeSerializer` should save validated input json blob to new db entries

        `dtype` should map to new `DataType` entry if it doesn't already exist
        '''

        serializer = serializers.AttributeSerializer(data=self.json_blob)

        # We need to call `is_valid()` before saving the entry
        serializer.is_valid()

        serializer.save()

        self.assertTrue(models.DataType.objects.all().exists())

    def test_serializer_deserializes_data_correctly_creates_attribute(self):
        '''
        `AttributeSerializer` should save validated input json blob to new db entries

        `name` should map to new `Attribute` entry if it doesn't already exist
        '''

        serializer = serializers.AttributeSerializer(data=self.json_blob)

        # We need to call `is_valid()` before saving the entry
        serializer.is_valid()

        serializer.save()

        self.assertTrue(models.Attribute.objects.all().exists())


class MeasureSerializerTests(TestCase):
    '''
    TestCase class for the `MeasureSerializer` serializer
    '''

    def setUp(self):
        '''
        Common setup for each test definition
        '''

        # Create an `Measure` entry
        dtype_tz = models.DataType.objects.create(name='timezone')
        self.measure = models.Measure.objects.create(
            name='published_date', measure_type='time', unit_of_measurement='TIMESTAMP',
            value_dtype=dtype_tz, statistic_type='observation (default)',
            measurement_reference_time='__self__', measurement_precision='±(default=NULL)'
        )

    def test_serializer_serializes_correctly(self):
        '''
        `MeasureSerializer` should serialize an input `Measure` entry to json in a format that
        agrees with the format defined at
        https://github.com/mister-one/onesto/blob/master/ABM/Book
        '''

        expected_json = {
            'measure_name': 'published_date',
            'measure_type': 'time',
            'unit_of_measurement': 'TIMESTAMP',
            'value_dtype': 'TIMEZONE',
            'statistic_type': 'observation (default)',
            'measurement_reference_time': '__self__',
            'measurement_precision': '±(default=NULL)'
        }

        serializer = serializers.MeasureSerializer(self.measure)

        self.assertDictEqual(serializer.data, expected_json)


class AMLinkSerializerTests(TestCase):
    '''
    TestCase class for the `AMLinkSerializer` serializer
    '''

    def setUp(self):
        '''
        Common setup for each test definition
        '''

        # Create an `AMLink` entry
        item_book = models.Item.objects.create(name='book')
        item_person = models.Item.objects.create(name='person')

        relationship_wrote = models.Relationship.objects.create(
            relationship_str='(Book)<-[WROTE]-(Person)'
        )
        relationship_wrote.item.add(item_book, item_person)

        self.link = models.AMLink.objects.create(
            relationship=relationship_wrote, instances_value_dtype='ABM/Person/1',
            time_link=False, link_criteria='best_rated',
            values=r'{"Person": {"name": "__input__"}}'
        )

    def test_serializer_serializes_correctly(self):
        '''
        `AMLinkSerializer` should serialize an input `AMLink` entry to json in a format that
        agrees with the format defined at
        https://github.com/mister-one/onesto/blob/master/ABM/Book
        '''

        expected_json = {
            'relationship': '(Book)<-[WROTE]-(Person)',
            'instances_value_dtype': 'ABM/Person/1',
            'time_link': False,
            'link_criteria': 'best_rated',
            'values': r'{"Person": {"name": "__input__"}}'
        }

        serializer = serializers.AMLinkSerializer(self.link)

        self.assertDictEqual(serializer.data, expected_json)

class AbstractModelSerializerTests(TestCase):
    '''
    TestCase class for the `AbstractModelSerializer` serializer
    '''

    maxDiff = None

    def setUp(self):
        '''
        Common setup for each test definition
        '''

        # Create an `AbstractModel` entry like the initial example given in
        # https://github.com/mister-one/onesto/blob/master/ABM/Book
        # item_book = models.Item.objects.create(name='book')
        # item_person = models.Item.objects.create(name='person')
        # item_review = models.Item.objects.create(name='review')

        # dtype_vchar = models.DataType.objects.create(name='varchar')
        # dtype_int = models.DataType.objects.create(name='int')
        # dtype_tz = models.DataType.objects.create(name='timezone')

        # attribute_1 = models.Attribute.objects.create(name='title', dtype=dtype_vchar)
        # attribute_2 = models.Attribute.objects.create(name='category', dtype=dtype_vchar)

        # measure_1 = models.Measure.objects.create(
        #     name='published_date', measure_type='time', unit_of_measurement='TIMESTAMP',
        #     value_dtype=dtype_int, statistic_type='observation (default)',
        #     measurement_reference_time='__self__', measurement_precision='±(default=NULL)'
        # )
        # measure_2 = models.Measure.objects.create(
        #     name='pages', measure_type='count', unit_of_measurement='Page',
        #     value_dtype=dtype_tz, statistic_type='observation (default)',
        #     measurement_reference_time='__self__', measurement_precision='±(default=NULL)'
        # )

        # relationship_wrote = models.Relationship.objects.create(
        #     relationship_str='(Book)<-[WROTE]-(Person)'
        # )
        # relationship_wrote.item.add(item_book, item_person)
        # relationship_about = models.Relationship.objects.create(
        #     relationship_str='(Book)<-[ABOUT]-(Review)'
        # )
        # relationship_about.item.add(item_book, item_review)

        # link_1 = models.AMLink.objects.create(
        #     relationship=relationship_wrote, instances_value_dtype='ABM/Person/1',
        #     time_link=False, link_criteria='best_rated',
        #     values=r'{"Person": {"name": "__input__"}}'
        # )
        # link_2 = models.AMLink.objects.create(
        #     relationship=relationship_about, instances_value_dtype='ABM/Review/1',
        #     time_link=False, link_criteria='direct',
        #     values=r'{"Review": {"title": "__input__", "score": "__input__"}}'
        # )

        # self.am_entry = models.AbstractModel.objects.create(master_item=item_book)
        # self.am_entry.attribute.add(attribute_1, attribute_2)
        # self.am_entry.measure.add(measure_1, measure_2)
        # self.am_entry.link.add(link_1, link_2)

        # Load the json blob defined at
        # https://github.com/mister-one/onesto/blob/master/ABM/Book
        with open(os.path.join(settings.BASE_DIR, 'doc', 'abm_input.json')) as f: # pylint: disable=invalid-name
            self.json_blob = json.load(f)

    # def test_serializer_serializes_correctly(self):
    #     '''
    #     `AbstractModelSerializer` should serialize an input `AbstractModel` entry to json in a
    #     format that agrees with the format defined at
    #     https://github.com/mister-one/onesto/blob/master/ABM/Book
    #     '''


    #     serializer = serializers.AbstractModelSerializer(self.am_entry)

    #     self.assertEqual(json.dumps(serializer.data), self.json_blob)

    def test_serializer_validates_data_correctly(self):
        '''
        `AbstractModelSerializer` should validate input json blob data as valid

        We need to call the `is_valid()` method before saving the data to new model entries
        '''

        serializer = serializers.AbstractModelSerializer(data=self.json_blob)

        self.assertTrue(serializer.is_valid())

    def test_serializer_deserializes_data_correctly_creates_item(self):
        '''
        `AbstractModelSerializer` should save validated input json blob to new db entries

        `master_item` should map to new `Item` entry if it doesn't already exist
        '''

        serializer = serializers.AbstractModelSerializer(data=self.json_blob)

        # We need to call `is_valid()` before saving the entry
        serializer.is_valid()

        serializer.save()

        # Check to see that this has created a new `Item` entry
        self.assertTrue(models.Item.objects.all().exists())
