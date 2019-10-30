# Generated by Django 2.2.6 on 2019-10-30 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0004_auto_20191030_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='division',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='custom_auth.Division'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='custom_auth.UserLevel'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='custom_auth.Organization'),
        ),
    ]
