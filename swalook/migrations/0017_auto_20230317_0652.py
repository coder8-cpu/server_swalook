# Generated by Django 4.0.6 on 2023-03-17 06:52

from django.db import migrations
from django.contrib.auth.models import User
def migrate_to_product_model(apps, schema_editor):
     user = User.objects.get(username="8459016262")
     service = apps.get_model('swalook', 'Service_data')
     for service in service.objects.all():
        service.user_id = user.id
        service.save()

class Migration(migrations.Migration):

    dependencies = [
        ('swalook', '0016_service_data_user'),
    ]

    operations = [
        migrations.RunPython(migrate_to_product_model)
    ]