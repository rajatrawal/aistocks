# Generated by Django 4.0.6 on 2022-07-24 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_symbol_symbol_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Signal',
        ),
        migrations.AddField(
            model_name='symbol',
            name='current_position',
            field=models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], default='buy', max_length=4),
        ),
        migrations.AlterField(
            model_name='symbol',
            name='symbol_id',
            field=models.UUIDField(default=191854808511362063029592340107769139930, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
