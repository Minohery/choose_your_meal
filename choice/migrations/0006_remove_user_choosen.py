# Generated by Django 3.1 on 2020-12-12 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('choice', '0005_auto_20201212_1438'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='choosen',
        ),
    ]