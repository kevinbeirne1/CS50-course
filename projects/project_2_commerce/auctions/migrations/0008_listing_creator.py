# Generated by Django 3.1.6 on 2021-04-21 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210421_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator', to='auctions.user'),
        ),
    ]