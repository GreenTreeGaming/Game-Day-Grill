# Generated by Django 4.2 on 2023-12-17 01:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_reservations'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reservations',
            new_name='Reservation',
        ),
    ]
