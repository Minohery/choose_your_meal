# Generated by Django 3.1 on 2020-12-12 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='choosen',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='user',
            name='command',
            field=models.BooleanField(default=False),
        ),
    ]