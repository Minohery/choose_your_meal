# Generated by Django 3.1 on 2020-12-12 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choice', '0010_auto_20201212_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='choosen',
            field=models.PositiveIntegerField(choices=[], default=0),
        ),
    ]