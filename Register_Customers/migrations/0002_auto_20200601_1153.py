# Generated by Django 3.0.5 on 2020-06-01 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Register_Customers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='Payment',
            new_name='Payments',
        ),
    ]
