# Generated by Django 5.1.2 on 2024-10-21 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0005_alter_cartticket_event_alter_cartticket_sector_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="image",
            field=models.ImageField(default=0, upload_to=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="hall",
            name="image",
            field=models.ImageField(default=0, upload_to=""),
            preserve_default=False,
        ),
    ]
