# Generated by Django 2.2 on 2020-04-14 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
