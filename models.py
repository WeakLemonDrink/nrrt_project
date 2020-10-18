from django.db import models


class DataType(models.Model):
    '''
    Defines db table for `DataType`s
    '''

    name = models.CharField(unique=True) # e.g. VARCHAR, MEASURE, INT etc

    def __str__(self):
        '''
        Defines the return string for an `Attribute` db table entry
        '''

        return self.name


class Attribute(models.Model):
    '''
    Defines db table for an `Attribute`
    '''

    attribute_name = models.CharField(unique=True) # Is this unique?
    value_dtype = models.ForeignKey(DataType)

    def serialize(self):
        '''
        Returns a entry serialized to json format (e.g. when constructing the returned data)
        '''

        pass

    def __str__(self):
        '''
        Defines the return string for an `Attribute` db table entry
        '''

        return self.attribute_name


class Measure(models.Model):
    '''
    Defines db table for a `Measure`
    '''

    measure_name = models.CharField()
    measure_type = models.CharField() # This could be limited to a choice if there are limited types,
                                      # or `ForeignKey` to a db table if you want to search/filter
                                      # by measure_type
    unit_of_measurement = models.CharField()
    value_dtype = models.ForeignKey(DataType)
    statistic_type = models.CharField() # This could be limited to a choice if there are limited
                                        # types, or `ForeignKey` to a db table if you want to
                                        # search/filter by statistic_type
    measurement_reference_time = models.CharField()
    measurement_precision = models.CharField()

    def serialize(self):
        '''
        Returns a entry serialized to json format (e.g. when constructing the returned data)
        '''

        pass

    def __str__(self):
        '''
        Defines the return string for an `Measure` db table entry
        '''

        return self.measure_name


# It may be better to combine `ABMLink` and `InstanceLink` tables into one `Link` table
# as the data looks common across both
class Link(models.Model):
    '''
    Defines db table for a `Link`
    '''

    relationship = models.CharField()
    instances_value_dtype = models.CharField()
    time_link = models.BooleanField()
    link_criteria = models.CharField()
    values = models.CharField() # Could also be a json field if this is dictionary like

    def serialize(self):
        '''
        Returns a entry serialized to json format (e.g. when constructing the returned data)
        '''

        pass

    def __str__(self):
        '''
        Defines the return string for an `ABMLink` db table entry
        '''

        return self.relationship


class AbstractBaseModel(models.Model):
    '''
    Defines db table for `AbstractBaseModel`
    '''

    name = models.CharField() # Not unique, but may be useful to `ForeignKey` this so you can link
                              # ABM entries together
    attribute = models.ManyToOneField(Attribute)
    measure = models.ManyToOneField(Measure)
    link = models.ManyToOneField(ABMLink)

    def serialize(self):
        '''
        Returns a entry serialized to json format (e.g. when constructing the returned data),
        using methods defined in related entries
        '''

        return_data = {
            'ABM_ID': self.id,
            'ATTR': [],
            'MEAS': [],
            'LINK': []
        }

        for attribute in self.attribute.objects.all():
            return_data['ATTR'].append(attribute.serialize())

        for measure in self.measure.objects.all():
            return_data['MEAS'].append(measure.serialize())

        for link in self.link.objects.all():
            return_data['LINK'].append(link.serialize())

        return return_data

    def __str__(self):
        '''
        Defines the return string for an `AbstractBaseModel` db table entry
        '''

        return self.name


# See `ABMLink` above
class InstanceLink(models.Model):
    '''
    Defines db table for `InstanceLink`
    '''

    relationship = models.CharField()
    landing_instance = models.CharField() # Could be a `models.UrlField` if this is always a url

    def serialize(self):
        '''
        Returns a entry serialized to json format (e.g. when constructing the returned data)
        '''

        pass

    def __str__(self):
        '''
        Defines the return string for an `InstanceLink` db table entry
        '''

        return self.relationship


# Need a bit more information on what a `Link` and a `IncomingInteractionLink` are
class IncomingInteractionLink(models.Model):
    '''
    Defines db table for `IncomingInteractionLink`
    '''

    relationship = models.CharField()
    origin_instance = models.CharField() # Could be a `models.UrlField` if this is always a url

    def serialize(self):
        '''
        Returns a entry serialized to json format (e.g. when constructing the returned data)
        '''

        pass

    def __str__(self):
        '''
        Defines the return string for an `IncomingInteractionLink` db table entry
        '''

        return self.relationship


class Instance(models.Model):
    '''
    Defines db table for `Instance`
    '''

    abm = models.ForeignKey(AbstractBaseModel)
    attribute = models.JsonField()
    measure = models.JsonField()
    link = models.ManyToOneField(InstanceLink) # e.g. (Book)<-[WROTE]-(Person)
    iil = models.ManyToOneField(IncomingInteractionLink)

    def serialize(self):
        '''
        Returns a entry serialized to json format (e.g. when constructing the returned data),
        using methods defined in related entries
        '''

        return_data = {
            'ABM': str(self.abm),
            'ATTR': self.attribute,
            'MEAS': self.measure,
            'LINK': [],
            'IIL': []
        }

        for link in self.link.objects.all():
            return_data['LINK'].append(link.serialize())

        for iil in self.iil.objects.all():
            return_data['IIL'].append(iil.serialize())

        return return_data


class RankingCluster(models.Model):
    '''
    Defines db table for `RankingCluster`
    '''

