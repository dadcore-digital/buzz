# Generated by Django 3.1 on 2021-02-27 20:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('players', '0011_auto_20210227_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player', to=settings.AUTH_USER_MODEL),
        ),
    ]
