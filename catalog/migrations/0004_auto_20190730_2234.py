# Generated by Django 2.2.3 on 2019-07-30 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20190730_2201'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['author']},
        ),
    ]
