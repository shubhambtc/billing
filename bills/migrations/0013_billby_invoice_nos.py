from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0012_billdetail_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='billby',
            name='invoice_nos',
            field=models.JSONField(default=dict),
        ),
    ]