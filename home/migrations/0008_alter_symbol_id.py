# Generated by Django 4.0.6 on 2022-07-22 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_symbol_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symbol',
            name='id',
            field=models.UUIDField(default='urn:uuid:a6aa62f0-78df-4874-ab2b-c75b116091a9', editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
