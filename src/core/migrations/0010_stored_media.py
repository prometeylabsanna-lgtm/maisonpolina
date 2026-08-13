from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_admin_russian_field_labels"),
    ]

    operations = [
        migrations.CreateModel(
            name="StoredMedia",
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
                (
                    "name",
                    models.CharField(db_index=True, max_length=255, unique=True),
                ),
                ("content", models.BinaryField()),
                (
                    "content_type",
                    models.CharField(blank=True, default="", max_length=64),
                ),
                ("size", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Файл",
                "verbose_name_plural": "Файлы",
            },
        ),
    ]
