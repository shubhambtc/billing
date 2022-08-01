
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0007_alter_billdetail_expenses'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dara',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateField()),
                ('loading_date', models.DateField()),
                ('vehicle_no', models.CharField(blank=True, default='', max_length=255)),
                ('dara', models.JSONField(blank=True, default=list, null=True)),
                ('weight', models.FloatField()),
                ('rate', models.FloatField()),
                ('bill_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bills.billto')),
            ],
        ),
    ]