# Generated by Django 3.1 on 2021-02-08 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0002_auto_20210128_2334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='program',
            name='mill',
        ),
    ]