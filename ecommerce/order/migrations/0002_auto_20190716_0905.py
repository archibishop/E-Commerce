# Generated by Django 2.2.3 on 2019-07-16 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='items',
            field=models.CharField(max_length=1000),
        ),
    ]