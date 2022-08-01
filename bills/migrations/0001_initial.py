import billsystem.storage_backends
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BillBy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('gstin', models.CharField(max_length=255)),
                ('mobile1', models.CharField(max_length=10)),
                ('mobile2', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=255)),
                ('state', models.CharField(blank=True, default='uttar pradesh', max_length=255)),
                ('state_code', models.IntegerField(blank=True, default=9)),
                ('bank_name', models.CharField(max_length=255)),
                ('bank_account_no', models.CharField(max_length=255)),
                ('bank_ifsc', models.CharField(max_length=255)),
                ('bank_branch', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='BillDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('vehicle_no', models.CharField(max_length=255)),
                ('remarks', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('bw', models.CharField(choices=[('A', 'A'), ('B', 'B')], default='A', max_length=255)),
                ('frieght', models.IntegerField(default=0)),
                ('invoice', models.FileField(blank=True, default=None, null=True, storage=billsystem.storage_backends.OverwriteStorage(), upload_to='invoices')),
                ('bill_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bills.billby')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tulai', models.FloatField(blank=True, default=0, null=True)),
                ('dharmada', models.FloatField(blank=True, default=0, null=True)),
                ('wages', models.FloatField(blank=True, default=0, null=True)),
                ('mandi_shulk', models.FloatField(blank=True, default=0, null=True)),
                ('sutli', models.FloatField(blank=True, default=0, null=True)),
                ('commision', models.FloatField(blank=True, default=0, null=True)),
                ('loading_charges', models.FloatField(blank=True, default=0, null=True)),
                ('vikas_shulk', models.FloatField(blank=True, default=0, null=True)),
                ('others', models.FloatField(blank=True, default=0, null=True)),
                ('bardana', models.FloatField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BillTo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('state_code', models.CharField(max_length=255)),
                ('gstin', models.CharField(blank=True, max_length=255, null=True)),
                ('bill_type', models.CharField(choices=[('MandiIn', 'MandiIn'), ('MandiOut', 'MandiOut')], max_length=255)),
                ('expense', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bills.expense')),
            ],
        ),
        migrations.CreateModel(
            name='BillItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=255)),
                ('rate', models.IntegerField()),
                ('qty', models.FloatField()),
                ('uom', models.IntegerField(blank=True, default=100)),
                ('po_number', models.CharField(default='', max_length=255)),
                ('bill_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bills.billdetail')),
            ],
        ),
        migrations.AddField(
            model_name='billdetail',
            name='bill_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bills.billto'),
        ),
    ]