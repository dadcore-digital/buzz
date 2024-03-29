# Generated by Django 3.1 on 2021-03-18 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0013_iglplayerlookup'),
    ]

    operations = [
        migrations.AddField(
            model_name='iglplayerlookup',
            name='discord_avatar_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='iglplayerlookup',
            name='discord_nick',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='iglplayerlookup',
            name='igl_player_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
