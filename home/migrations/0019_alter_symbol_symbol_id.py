# Generated by Django 4.0.6 on 2022-07-26 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_alter_symbol_symbol_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symbol',
            name='symbol_id',
            field=models.UUIDField(default='urn:uuid:9ba30dc8-a87f-411a-a460-864265170d02', editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
