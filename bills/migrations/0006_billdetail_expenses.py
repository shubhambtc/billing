
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0005_auto_20210929_0917'),
    ]

    operations = [
        migrations.AddField(
            model_name='billdetail',
            name='expenses',
            field=models.JSONField(blank=True, default={}, null=True),
        ),
    ]