# Generated by Django 2.1.5 on 2019-03-01 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='story',
            unique_together={('story_headline', 'story_details')},
        ),
    ]