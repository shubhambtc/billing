# Generated by Django 3.2.7 on 2022-06-14 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderparty',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='orderparty',
            name='contact_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='orderparty',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]