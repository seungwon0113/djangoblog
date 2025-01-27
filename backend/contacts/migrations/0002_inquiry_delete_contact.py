# Generated by Django 5.1.5 on 2025-01-27 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contacts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Inquiry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=255)),
                ("message", models.TextField()),
            ],
            options={
                "verbose_name": "Inquiry",
                "verbose_name_plural": "Inquiries",
                "db_table": "inquiries",
            },
        ),
        migrations.DeleteModel(
            name="Contact",
        ),
    ]
