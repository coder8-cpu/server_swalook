# Generated by Django 4.0.6 on 2023-05-13 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swalook', '0022_staff_account_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff_account_details',
            name='staffname',
            field=models.CharField(default=0, max_length=1000),
            preserve_default=False,
        ),
    ]