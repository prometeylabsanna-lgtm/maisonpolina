from django.db import migrations, models

LOCATION_RU = "вул. Феодосія Печерського, 1, Ходосівка, Київська область, 08173"
LOCATION_EN = "1 Feodosiia Pecherskyi St, Khodosivka, Kyiv Oblast, 08173"
COMPANY = "MaisonPolina"
PLACEHOLDER_EMAILS = ("hello@example.com", "admin@example.com", "")


def apply_legal(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    for row in SiteSettings.objects.all():
        row.company_legal_name = COMPANY
        row.copyright_name = COMPANY
        row.location_ru = LOCATION_RU
        row.location_en = LOCATION_EN
        if (row.email or "").strip().lower() in PLACEHOLDER_EMAILS:
            row.email = ""
        row.save(
            update_fields=[
                "company_legal_name",
                "copyright_name",
                "location_ru",
                "location_en",
                "email",
            ]
        )


def revert_legal(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    SiteSettings.objects.all().update(
        company_legal_name="",
        copyright_name="MAISON POLINA",
        location_ru="ЖК «Нова Конча-Заспа»",
        location_en="Nova Koncha-Zaspa RC",
        email="hello@example.com",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_phone_whatsapp_hide_facts"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="company_legal_name",
            field=models.CharField(
                blank=True,
                default="MaisonPolina",
                max_length=255,
                verbose_name="Юридическое название компании",
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="copyright_name",
            field=models.CharField(
                default="MaisonPolina",
                max_length=128,
                verbose_name="Имя в копирайте",
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="email",
            field=models.EmailField(
                blank=True,
                default="",
                max_length=254,
                verbose_name="Email",
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="location_ru",
            field=models.CharField(
                blank=True,
                default=LOCATION_RU,
                max_length=255,
                verbose_name="Адрес / локация",
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="location_en",
            field=models.CharField(
                blank=True,
                default=LOCATION_EN,
                max_length=255,
                verbose_name="Адрес / локация",
            ),
        ),
        migrations.RunPython(apply_legal, revert_legal),
    ]
