# Generated by Django 4.0.6 on 2022-07-22 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_symbol_symbol_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symbol',
            name='symbol_id',
            field=models.UUIDField(default=124071781346350200480112770304685991567, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
