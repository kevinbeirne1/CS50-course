# Generated by Django 3.1.6 on 2021-04-20 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20210420_1437'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'ordering': ['-listing', '-amount']},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-listing', '-comment_date']},
        ),
        migrations.AlterModelOptions(
            name='listing',
            options={'ordering': ['pub_date']},
        ),
    ]
