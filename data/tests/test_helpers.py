'''
Tests for `data.helpers` in the `data` Django web app
'''


from django.test import TestCase

from data import helpers, models


class UpdateRankingClustersTests(TestCase):
    '''
    TestCase class for the `update_ranking_clusters` method
    '''

    fixtures = [
        './doc/instanceserializertests.xml'
    ]

    def test_method_creates_new_ranking_cluster(self):
        '''
        `update_ranking_clusters` method should update all instances with abm__master_item matching
        each `Item` in the input item queryset

        Method should create a new `RankingCluster` as one doesn't already exist
        '''

        # Create a `Item` queryset with a single item
        item_qs = models.Item.objects.filter(name='Award')

        helpers.update_ranking_clusters(item_qs)

        # `update_ranking_clusters` method should create a single ranking cluster
        self.assertEqual(models.RankingCluster.objects.all().count(), 1)

    def test_method_updates_existing_ranking_cluster(self):
        '''
        `update_ranking_clusters` method should update all instances with abm__master_item matching
        each `Item` in the input item queryset

        Method should update an existing `RankingCluster` if one already exists
        '''

        # Create a `Item` queryset with a single item
        award = models.Item.objects.get(name='Award')
        item_qs = models.Item.objects.filter(name='Award')

        # Create a ranking cluster
        models.RankingCluster.objects.create(master_item=award, ranking_feature='NULL')

        helpers.update_ranking_clusters(item_qs)

        # `update_ranking_clusters` method should not have created a new `RankingCluster`, just
        # updated the existing one
        self.assertEqual(models.RankingCluster.objects.all().count(), 1)

    def test_method_creates_multiple_ranking_clusters(self):
        '''
        `update_ranking_clusters` method should update all instances with abm__master_item matching
        each `Item` in the input item queryset

        Method should create a `RankingCluster` entry for each `Item` in the input item queryset
        '''

        # Create a `Item` queryset with all the items in the fixtures (3)
        item_qs = models.Item.objects.all()

        helpers.update_ranking_clusters(item_qs)

        # `update_ranking_clusters` method should create 3 ranking cluster entries
        self.assertEqual(models.RankingCluster.objects.all().count(), 3)

    def test_method_ranking_cluster_null_number_of_instances_filled(self):
        '''
        `update_ranking_clusters` method should create and populate `RankingCluster` entries for
        each `Item` in the input item queryset

        Method should populate the `number_of_instances` field with the number of related instances
        '''

        # Create a `Item` queryset with a single item
        award = models.Item.objects.get(name='Award')
        item_qs = models.Item.objects.filter(name='Award')

        helpers.update_ranking_clusters(item_qs)

        # `update_ranking_clusters` method should have created a new `RankingCluster` entry and
        entry = models.RankingCluster.objects.get(master_item=award, ranking_feature='NULL')

        # should save number_of_instances as 2
        self.assertEqual(entry.number_of_instances, 2)

    def test_method_ranking_cluster_null_instances_ranking_filled(self):
        '''
        `update_ranking_clusters` method should create and populate `RankingCluster` entries for
        each `Item` in the input item queryset

        Method should populate the `instances_ranking` field with the serialized instances
        '''

        expected_instances_ranking_data = [
            {
                "item": "Award",
                "id": 1,
                "abm": 1,
                "attribute": "{\"Year\": \"1928\"}",
                "measure": "",
                "link": []
            },
            {
                "item": "Award",
                "id": 4,
                "abm": 1,
                "attribute": "{\"Year\": \"1929\"}",
                "measure": "",
                "link": []
            },
        ]

        # Create a `Item` queryset with a single item
        award = models.Item.objects.get(name='Award')
        item_qs = models.Item.objects.filter(name='Award')

        helpers.update_ranking_clusters(item_qs)

        # `update_ranking_clusters` method should have created a new `RankingCluster` entry and
        entry = models.RankingCluster.objects.get(master_item=award, ranking_feature='NULL')

        # should save instances_ranking as serialized instances
        self.assertEqual(entry.instances_ranking, expected_instances_ranking_data)
