# Generated by Django 3.1 on 2020-11-12 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mill_procedure', '0002_auto_20201112_0233'),
    ]

    operations = [
        migrations.AddField(
            model_name='millprocedure',
            name='run_length',
            field=models.IntegerField(default=100000),
        ),
    ]