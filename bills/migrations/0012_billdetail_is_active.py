from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0011_auto_20220211_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='billdetail',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]