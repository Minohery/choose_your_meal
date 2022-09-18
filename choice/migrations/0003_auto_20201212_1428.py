# Generated by Django 3.1 on 2020-12-12 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choice', '0002_auto_20201212_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choices', models.CharField(max_length=150)),
                ('ref', models.PositiveIntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='choosen',
        ),
    ]