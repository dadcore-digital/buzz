# Generated by Django 3.1 on 2020-12-15 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casters', '0004_namemapping'),
    ]

    operations = [
        migrations.AddField(
            model_name='caster',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
