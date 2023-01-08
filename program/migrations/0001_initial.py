# Generated by Django 3.1 on 2021-01-28 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fabrics', '0004_auto_20210128_2316'),
        ('brand', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brand.brand')),
                ('fabric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fabrics.fabric')),
                ('mill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fabrics.mill')),
            ],
        ),
    ]