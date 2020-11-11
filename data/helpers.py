'''
Helper functions for the `data` Django application
'''


from data import models, serializers


def update_ranking_cluster_ranking_feature_null(item_qs):
    '''
    Loop through each `Item` entry in the input `item_qs` and:
     * Return all `Instance` entries linked to the `Item`
     * Serialize the returned `Instance` entries
     * Get or create a `RankingCluster` entry master_item=`Item` and ranking_features=None
     * Update the `instances_ranking` field with the serialized `Instance` entries
     * Return the `RankingCluster` entries?
    '''

    ranking_clusters = []

    for item in item_qs:
        # Grab the related `Instance` entries
        instance_qs = models.Instance.objects.filter(abm__master_item=item)

        # Get or create the `RankingCluster` entry with `ranking_features=None`
        ranking_cluster, _ = models.RankingCluster.objects.get_or_create(master_item=item,
                                                                         ranking_features=None)

        # Serialize the `instance_qs` and save to the `RankingCluster`
        serializer = serializers.InstanceSerializer(instance_qs, many=True)

        ranking_cluster.number_of_instances = instance_qs.count()
        ranking_cluster.instances_ranking = serializer.data
        ranking_cluster.save()

        # Append to return list
        ranking_cluster.append(ranking_clusters)

    return ranking_clusters
