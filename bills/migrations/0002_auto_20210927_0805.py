from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billdetail',
            name='vehicle_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='billitem',
            name='po_number',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]