# Generated by Django 2.2.6 on 2019-10-30 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0005_auto_20191030_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='division',
            name='is_default_division',
            field=models.BooleanField(default=False),
        ),
    ]
