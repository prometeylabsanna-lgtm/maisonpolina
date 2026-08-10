from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="testimonial",
            name="rating",
            field=models.PositiveSmallIntegerField(default=5),
        ),
        migrations.AddField(
            model_name="testimonial",
            name="is_public_submission",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="testimonial",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name="testimonial",
            name="text_ru",
            field=models.TextField(blank=True),
        ),
        migrations.AlterModelOptions(
            name="testimonial",
            options={
                "ordering": ["order", "-created_at", "pk"],
                "verbose_name": "Відгук",
                "verbose_name_plural": "Відгуки",
            },
        ),
    ]
