from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0006_billdetail_expenses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billdetail',
            name='expenses',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]