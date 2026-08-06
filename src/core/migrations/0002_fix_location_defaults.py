from django.db import migrations, models


def fix_ukrainian_location(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    for obj in SiteSettings.objects.all():
        if obj.location_ru in ("Київ, за домовленістю", "Москва, по договорённости", ""):
            obj.location_ru = "Киев, по договорённости"
        if obj.location_en in ("Kyiv, by arrangement", "Moscow, by arrangement", ""):
            obj.location_en = "Kyiv, by appointment"
        obj.save(update_fields=["location_ru", "location_en"])


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="location_ru",
            field=models.CharField(
                blank=True,
                default="Киев, по договорённости",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="location_en",
            field=models.CharField(
                blank=True,
                default="Kyiv, by appointment",
                max_length=255,
            ),
        ),
        migrations.RunPython(fix_ukrainian_location, migrations.RunPython.noop),
    ]
