# Generated by Django 3.1 on 2021-04-03 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0025_auto_20210403_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='circuit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='leagues.circuit'),
        ),
    ]