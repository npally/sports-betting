# Generated by Django 2.2.6 on 2019-11-02 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0006_pick_wager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pick',
            name='wager',
            field=models.FloatField(default=0, null=True),
        ),
    ]
