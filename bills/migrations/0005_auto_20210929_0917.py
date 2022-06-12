from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0004_auto_20210929_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billdetail',
            name='bill_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bills.billby'),
        ),
        migrations.AlterField(
            model_name='billdetail',
            name='bill_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bills.billto'),
        ),
    ]