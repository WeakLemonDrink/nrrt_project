# Generated by Django 3.1.2 on 2020-11-12 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rankingcluster',
            name='instances_ranking',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rankingcluster',
            name='links_ranking',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rankingcluster',
            name='ranking_feature',
            field=models.JSONField(default='NULL'),
            preserve_default=False,
        ),
    ]
