# Generated by Django 4.0.6 on 2022-07-26 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_alter_symbol_symbol_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symbol',
            name='symbol_id',
            field=models.CharField(default='urn:uuid:f3156b87-46f4-44c0-b360-1cf659d28cd3', editable=False, max_length=500, primary_key=True, serialize=False, unique=True),
        ),
    ]
