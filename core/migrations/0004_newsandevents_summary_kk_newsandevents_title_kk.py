# Generated by Django 4.0.8 on 2025-03-28 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_newsandevents_summary_es_newsandevents_summary_fr_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsandevents',
            name='summary_kk',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='newsandevents',
            name='title_kk',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
