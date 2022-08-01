# Generated by Django 3.2.7 on 2022-07-27 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_unloadingorders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loadingunloading',
            name='unloaded_to',
            field=models.ManyToManyField(blank=True, related_name='unloaded_party', to='orders.OrderParty'),
        ),
    ]