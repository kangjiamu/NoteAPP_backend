# Generated by Django 4.2.5 on 2024-06-06 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("notes", "0002_alter_tag_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="note",
            name="tags",
        ),
        migrations.AddField(
            model_name="note",
            name="tags",
            field=models.JSONField(default=list),
        ),
    ]