# Generated by Django 4.0.6 on 2022-07-24 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_symbol_symbol_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signal',
            name='status',
            field=models.CharField(blank=True, choices=[('active', 'Active'), ('failed', 'Failed'), ('successful', 'Successful')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='symbol',
            name='symbol_id',
            field=models.UUIDField(default=155831690366726129508371059436919111918, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
