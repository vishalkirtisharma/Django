# Generated by Django 5.1.5 on 2025-01-28 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf', '0002_profilemodel_degree'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilemodel',
            name='summary',
            field=models.TextField(blank=True, null=True),
        ),
    ]
