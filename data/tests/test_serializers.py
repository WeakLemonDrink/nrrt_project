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

    def test_serializer_deserializes_data_correctly_creates_attribute_many(self):
        '''
        `AttributeSerializer` should save validated input json blob to new db entries

        a blob containing multiple instances should create multiple entries
        '''

        # Create blob containing two entries
        json_blob = [
            self.json_blob,
            {
                'attribute_name': 'category',
                'value_dtype': 'VARCHAR'
            },
        ]

        serializer = serializers.AttributeSerializer(data=json_blob, many=True)

        # We need to call `is_valid()` before saving the entry
        serializer.is_valid()

        serializer.save()

        # Serializer should create two new entries
        self.assertEqual(models.Attribute.objects.count(), 2)


class MeasureSerializerTests(TestCase):
    '''
    TestCase class for the `MeasureSerializer` serializer
    '''

    def setUp(self):
        '''
        Common setup for each test definition
        '''

        self.json_blob = {
            'measure_name': 'published_date',
            'measure_type': 'time',
            'unit_of_measurement': 'TIMESTAMP',
            'value_dtype': 'TIMEZONE',
            'statistic_type': 'observation (default)',
            'measurement_reference_time': '__self__',
            'measurement_precision': '±(default=NULL)'
        }

    def test_serializer_serializes_correctly(self):
        '''
        `MeasureSerializer` should serialize an input `Measure` entry to json in a format that
        agrees with the format defined at
        https://github.com/mister-one/onesto/blob/master/ABM/Book
        '''

        # Create an `Measure` entry
        dtype_tz = models.DataType.objects.create(name='timezone')
        measure = models.Measure.objects.create(
            name='published_date', measure_type='time', unit_of_measurement='TIMESTAMP',
            value_dtype=dtype_tz, statistic_type='observation (default)',
            measurement_reference_time='__self__', measurement_precision='±(default=NULL)'
        )

        serializer = serializers.MeasureSerializer(measure)

        self.assertDictEqual(serializer.data, self.json_blob)

    def test_serializer_deserializes_data_correctly_creates_data_type(self):
        '''
        `MeasureSerializer` should save validated input json blob to new db entries

        `value_dtype` should map to new `DataType` entry if it doesn't already exist
        '''

        serializer = serializers.MeasureSerializer(data=self.json_blob)

        # We need to call `is_valid()` before saving the entry
        serializer.is_valid()

        serializer.save()

        self.assertTrue(models.DataType.objects.all().exists())

    def test_serializer_deserializes_data_correctly_creates_measure(self):
        '''
        `MeasureSerializer` should save validated input json blob to new db entries

        Other fields should map to new `Measure` entry if it doesn't already exist
        '''

        serializer = serializers.MeasureSerializer(data=self.json_blob)

        # We need to call `is_valid()` before saving the entry
        serializer.is_valid()

        serializer.save()

        self.assertTrue(models.Measure.objects.all().exists())

    def test_serializer_deserializes_data_correctly_creates_attribute_many(self):
        '''
        `MeasureSerializer` should save validated input json blob to new db entries

        a blob containing multiple instances should create multiple entries
        '''

        # Create blob containing two entries
        json_blob = [
            self.json_blob,
            {
                'measure_name': 'published_date',
                'measure_type': 'time',
                'unit_of_measurement': 'TIMESTAMP',
                'value_dtype': 'TIMESTAMP',
                'statistic_type': 'observation (default)',
                'measurement_reference_time': '__self__',
                'measurement_precision': '±(default=NULL)'
            },
        ]

        serializer = serializers.MeasureSerializer(data=json_blob, many=True)

        # We need to call `is_valid()` before saving the entry
        serializer.is_valid()

        serializer.save()

        # Serializer should create two new entries
        self.assertEqual(models.Measure.objects.count(), 2)


class AMLinkSerializerTests(TestCase):
    '''
    TestCase class for the `AMLinkSerializer` serializer
    '''

    def setUp(self):
        '''
        Common setup for each test definition
        '''

        self.json_blob = {
            'relationship': '(Book)<-[WROTE]-(Person)',
            'instances_value_dtype': 'ABM/Person/1',
            'time_link': False,
            'link_criteria': 'best_rated',
            'values': r'{"Person": {"name": "__input__"}}'
        }

    def test_serializer_serializes_correctly(self):
        '''
        `AMLinkSerializer` should serialize an input `AMLink` entry to json in a format that
        agrees with the format defined at
        https://github.com/mister-one/onesto/blob/master/ABM/Book
        '''

        # Create an `AMLink` entry
        relationship_wrote = models.Relationship.objects.create(
            relationship_str='(Book)<-[WROTE]-(Person)'
        )

        link = models.AMLink.objects.create(
            relationship=relationship_wrote, instances_value_dtype='ABM/Person/1',
            time_link=False, link_criteria='best_rated',
            values=r'{"Person": {"name": "__input__"}}'
        )

        serializer = serializers.AMLinkSerializer(link)

        self.assertDictEqual(serializer.data, self.json_blob)

    def test_serializer_deserializes_data_correctly_creates_relationship(self):
        '''
        `AMLinkSerializer` should save validated input json blob to new db entries

        `relationship` should map to new `Relationship` entry if it doesn't already exist
        '''

        serializer = serializers.AMLinkSerializer(data=self.json_blob)

        # We need to call `is_valid()` before saving the entry
        serializer.is_valid()

        serializer.save()

        self.assertTrue(models.Relationship.objects.all().exists())

    def test_serializer_deserializes_data_correctly_creates_amlink(self):
        '''
        `AMLinkSerializer` should save validated input json blob to new db entries

        Other fields should map to new `Measure` entry if it doesn't already exist
        '''

        serializer = serializers.AMLinkSerializer(data=self.json_blob)

        # We need to call `is_valid()` before saving the entry
        serializer.is_valid()

        serializer.save()

        self.assertTrue(models.AMLink.objects.all().exists())

    def test_serializer_deserializes_data_correctly_creates_amlink_many(self):
        '''
        `AMLinkSerializer` should save validated input json blob to new db entries

        a blob containing multiple instances should create multiple entries
        '''

        # Create blob containing two entries
        json_blob = [
            self.json_blob,
            {
                'relationship': '(Book)<-[ABOUT]-(Review)',
                'instances_value_dtype': 'ABM/Review/1',
                'time_link': False,
                'link_criteria': 'direct',
                'values': r'{"Review": {"title": "__input__", "score": "__input__"}}'
        },
        ]

        serializer = serializers.AMLinkSerializer(data=json_blob, many=True)

        # We need to call `is_valid()` before saving the entry
        serializer.is_valid()

        serializer.save()

        # Serializer should create two new entries
        self.assertEqual(models.AMLink.objects.count(), 2)


class AbstractModelSerializerTests(TestCase):
    '''
    TestCase class for the `AbstractModelSerializer` serializer
    '''

    maxDiff = None

    def setUp(self):
        '''
        Common setup for each test definition
        '''

        # Load the json blob defined at
        # https://github.com/mister-one/onesto/blob/master/ABM/Book
        with open(os.path.join(settings.BASE_DIR, 'doc', 'abm_input.json')) as f: # pylint: disable=invalid-name
            self.json_blob = json.load(f)

    def test_serializer_serializes_correctly(self):
        '''
        `AbstractModelSerializer` should serialize an input `AbstractModel` entry to json in a
        format that agrees with the format defined at
        https://github.com/mister-one/onesto/blob/master/ABM/Book
        '''

        # Create an `AbstractModel` entry like the initial example given in
        # https://github.com/mister-one/onesto/blob/master/ABM/Book
        item_book = models.Item.objects.create(name='book')

        dtype_vchar = models.DataType.objects.create(name='varchar')
        dtype_int = models.DataType.objects.create(name='int')
        dtype_tz = models.DataType.objects.create(name='timezone')

        attribute_1 = models.Attribute.objects.create(name='title', dtype=dtype_vchar)
        attribute_2 = models.Attribute.objects.create(name='category', dtype=dtype_vchar)

        measure_1 = models.Measure.objects.create(
            name='published_date', measure_type='time', unit_of_measurement='TIMESTAMP',
            value_dtype=dtype_int, statistic_type='observation (default)',
            measurement_reference_time='__self__', measurement_precision='±(default=NULL)'
        )
        measure_2 = models.Measure.objects.create(
            name='pages', measure_type='count', unit_of_measurement='Page',
            value_dtype=dtype_tz, statistic_type='observation (default)',
            measurement_reference_time='__self__', measurement_precision='±(default=NULL)'
        )

        relationship_wrote = models.Relationship.objects.create(
            relationship_str='(Book)<-[WROTE]-(Person)'
        )
        relationship_about = models.Relationship.objects.create(
            relationship_str='(Book)<-[ABOUT]-(Review)'
        )

        link_1 = models.AMLink.objects.create(
            relationship=relationship_wrote, instances_value_dtype='ABM/Person/1',
            time_link=False, link_criteria='best_rated',
            values=r'{"Person": {"name": "__input__"}}'
        )
        link_2 = models.AMLink.objects.create(
            relationship=relationship_about, instances_value_dtype='ABM/Review/1',
            time_link=False, link_criteria='direct',
            values=r'{"Review": {"title": "__input__", "score": "__input__"}}'
        )

        am_entry = models.AbstractModel.objects.create(master_item=item_book)
        am_entry.attribute.add(attribute_1, attribute_2)
        am_entry.measure.add(measure_1, measure_2)
        am_entry.link.add(link_1, link_2)

        serializer = serializers.AbstractModelSerializer(am_entry)

        self.assertDictEqual(serializer.data, self.json_blob)

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

    def test_serializer_deserializes_data_correctly_creates_attributes(self):
        '''
        `AbstractModelSerializer` should save validated input json blob to new db entries

        Input json blob should create two new `Attribute` entries
        '''

        serializer = serializers.AbstractModelSerializer(data=self.json_blob)

        # We need to call `is_valid()` before saving the entry
        serializer.is_valid()

        serializer.save()

        # Check to see that this has created 2 new `Attribute` entries
        self.assertEqual(models.Attribute.objects.all().count(), 2)

    def test_serializer_deserializes_data_correctly_creates_measures(self):
        '''
        `AbstractModelSerializer` should save validated input json blob to new db entries

        Input json blob should create two new `Measure` entries
        '''

        serializer = serializers.AbstractModelSerializer(data=self.json_blob)

        # We need to call `is_valid()` before saving the entry
        serializer.is_valid()

        serializer.save()

        # Check to see that this has created 2 new `Measure` entries
        self.assertEqual(models.Measure.objects.all().count(), 2)

    def test_serializer_deserializes_data_correctly_creates_amlinks(self):
        '''
        `AbstractModelSerializer` should save validated input json blob to new db entries

        Input json blob should create two new `AMLink` entries
        '''

        serializer = serializers.AbstractModelSerializer(data=self.json_blob)

        # We need to call `is_valid()` before saving the entry
        serializer.is_valid()

        serializer.save()

        # Check to see that this has created 2 new `AMLink` entries
        self.assertEqual(models.AMLink.objects.all().count(), 2)

    def test_serializer_deserializes_data_correctly_creates_abstractmodel(self):
        '''
        `AbstractModelSerializer` should save validated input json blob to new db entries

        Input json blob should create a new `AbstractModel` entry
        '''

        serializer = serializers.AbstractModelSerializer(data=self.json_blob)

        # We need to call `is_valid()` before saving the entry
        serializer.is_valid()

        serializer.save()

        # Check to see that this has created a new `AbstractModel` entries
        self.assertTrue(models.AbstractModel.objects.all().exists())

    def test_serializer_deserializes_data_correctly_creates_attribute_m2m(self):
        '''
        `AbstractModelSerializer` should save validated input json blob to new db entries

        Input json blob should create a new `AbstractModel` entry with two `Attribute` entries as a
        `ManyToMany` relationshp
        '''

        serializer = serializers.AbstractModelSerializer(data=self.json_blob)

        # We need to call `is_valid()` before saving the entry
        serializer.is_valid()

        entry = serializer.save()

        # Check to see that this has created a new `AbstractModel` entry with 2 `Attribute`
        # entries m2m
        self.assertEqual(entry.attribute.all().count(), 2)

    def test_serializer_deserializes_data_correctly_creates_measure_m2m(self):
        '''
        `AbstractModelSerializer` should save validated input json blob to new db entries

        Input json blob should create a new `AbstractModel` entry with two `Measure` entries as a
        `ManyToMany` relationshp
        '''

        serializer = serializers.AbstractModelSerializer(data=self.json_blob)

        # We need to call `is_valid()` before saving the entry
        serializer.is_valid()

        entry = serializer.save()

        # Check to see that this has created a new `AbstractModel` entry with 2 `Measure`
        # entries m2m
        self.assertEqual(entry.measure.all().count(), 2)

    def test_serializer_deserializes_data_correctly_creates_link_m2m(self):
        '''
        `AbstractModelSerializer` should save validated input json blob to new db entries

        Input json blob should create a new `AbstractModel` entry with two `Link` entries as a
        `ManyToMany` relationshp
        '''

        serializer = serializers.AbstractModelSerializer(data=self.json_blob)

        # We need to call `is_valid()` before saving the entry
        serializer.is_valid()

        entry = serializer.save()

        # Check to see that this has created a new `AbstractModel` entry with 2 `Link`
        # entries m2m
        self.assertEqual(entry.link.all().count(), 2)
