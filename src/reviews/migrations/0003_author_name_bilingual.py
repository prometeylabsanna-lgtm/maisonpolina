from django.db import migrations, models

# Known seed authors: Cyrillic → Latin for EN locale
_EN_NAMES = {
    "Дмитрий К.": "Dmitry K.",
    "Александр Г.": "Alexander G.",
    "Андрей М.": "Andrey M.",
    "Марина Т.": "Marina T.",
    "Ольга Р.": "Olga R.",
}


def forwards_fill_en_names(apps, schema_editor):
    Testimonial = apps.get_model("reviews", "Testimonial")
    for item in Testimonial.objects.all():
        ru = (item.author_name_ru or "").strip()
        if item.author_name_en:
            continue
        item.author_name_en = _EN_NAMES.get(ru, ru)
        item.save(update_fields=["author_name_en"])


def backwards_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0002_rating_moderation"),
    ]

    operations = [
        migrations.RenameField(
            model_name="testimonial",
            old_name="author_name",
            new_name="author_name_ru",
        ),
        migrations.AddField(
            model_name="testimonial",
            name="author_name_en",
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.RunPython(forwards_fill_en_names, backwards_noop),
    ]
