# Generated by Django 3.1 on 2021-05-23 00:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0011_auto_20210505_2113'),
        ('matches', '0029_game_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='away',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='away_matches', to='teams.team'),
        ),
        migrations.AlterField(
            model_name='result',
            name='status',
            field=models.CharField(choices=[('C', 'Completed'), ('SF', 'Single Forfeit'), ('DF', 'Double Forfeit'), ('BY', 'Bye')], max_length=2),
        ),
    ]