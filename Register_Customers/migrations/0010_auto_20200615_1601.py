# Generated by Django 3.0.5 on 2020-06-15 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Register_Customers', '0009_customerdetails_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerdetails',
            name='Email',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='Mobile',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='Username',
            field=models.EmailField(max_length=200),
        ),
        migrations.AlterField(
            model_name='customerdetails',
            name='password',
            field=models.CharField(max_length=200),
        ),
    ]
