# Generated by Django 4.0.6 on 2022-07-26 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_alter_signal_time_alter_symbol_symbol_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symbol',
            name='symbol',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='symbol',
            name='symbol_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
