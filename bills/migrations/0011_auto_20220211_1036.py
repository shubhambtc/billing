from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0010_auto_20220123_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='billdetail',
            name='gstdetail',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='billdetail',
            name='expenses',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='billdetail',
            name='shipto',
            field=models.JSONField(default=dict),
        ),
    ]