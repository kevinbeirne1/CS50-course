# Generated by Django 3.1.6 on 2021-04-26 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_listing_creator'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-listing', 'comment_date']},
        ),
        migrations.AlterField(
            model_name='bid',
            name='amount',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='listing',
            name='starting_bid',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
