# Generated by Django 3.1.7 on 2021-05-11 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfileapp', '0003_auto_20210511_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extension',
            name='is_extension',
            field=models.CharField(choices=[('image', 'Image'), ('pdf', 'PDF'), ('text', 'Text')], default='image', max_length=10),
        ),
    ]