# Generated by Django 3.1 on 2020-12-07 01:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
        ('casters', '0001_initial'),
        ('matches', '0003_auto_20201207_0122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='secondary_casters',
        ),
        migrations.AddField(
            model_name='match',
            name='secondary_casters',
            field=models.ManyToManyField(blank=True, null=True, related_name='cocasted_matches', to='casters.Caster'),
        ),
        migrations.RemoveField(
            model_name='match',
            name='winner',
        ),
        migrations.AddField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='won_matches', to='teams.team'),
        ),
    ]
