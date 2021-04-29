# Generated by Django 3.1 on 2021-04-29 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0026_auto_20210403_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='current_round',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_round_season', to='leagues.round'),
        ),
    ]
