# Generated by Django 2.2 on 2020-04-14 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20200414_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='hsn',
            field=models.CharField(max_length=12),
        ),
    ]
