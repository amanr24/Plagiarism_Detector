# Generated by Django 3.1.7 on 2021-05-11 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfileapp', '0006_auto_20210511_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuploadfile',
            name='myfiles',
            field=models.FileField(upload_to=''),
        ),
    ]
