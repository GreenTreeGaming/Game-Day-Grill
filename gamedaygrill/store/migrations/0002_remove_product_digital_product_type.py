# Generated by Django 4.2 on 2023-12-16 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='digital',
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('A', 'Appetizer'), ('MC', 'Main Course'), ('D', 'Dessert'), ('S', 'Side'), ('E', 'Extras')], max_length=2, null=True),
        ),
    ]
