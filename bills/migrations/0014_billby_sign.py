from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0013_billby_invoice_nos'),
    ]

    operations = [
        migrations.AddField(
            model_name='billby',
            name='sign',
            field=models.ImageField(blank=True, null=True, upload_to='sign'),
        ),
    ]