# Generated by Django 3.1 on 2021-06-07 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0028_auto_20210429_2031'),
        ('awards', '0007_awardcategory_discord_emoji'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='awards', to='leagues.group'),
        ),
    ]
