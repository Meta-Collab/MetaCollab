# Generated by Django 5.0.3 on 2024-04-20 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_alter_room_roomuuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="roomuuid",
            field=models.IntegerField(unique=True),
        ),
    ]
