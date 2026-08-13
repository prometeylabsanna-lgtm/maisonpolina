from django.db import migrations, models

PHONE = "+380 95 472 7859"
WHATSAPP_URL = "https://wa.me/qr/ZPQAL5UEFCQIN1"
HIDE_RU = ("Обувь", "Одежда", "Зодиак", "Тату", "Пирсинг")
HIDE_EN = ("Shoes", "Clothing", "Zodiac", "Tattoo", "Piercing")


def apply_site_content(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    PersonalityItem = apps.get_model("core", "PersonalityItem")
    SiteSettings.objects.filter(pk=1).update(
        phone=PHONE,
        whatsapp_url=WHATSAPP_URL,
    )
    PersonalityItem.objects.filter(label_ru__in=HIDE_RU).update(is_active=False)
    PersonalityItem.objects.filter(label_en__in=HIDE_EN).update(is_active=False)


def revert_site_content(apps, schema_editor):
    SiteSettings = apps.get_model("core", "SiteSettings")
    PersonalityItem = apps.get_model("core", "PersonalityItem")
    SiteSettings.objects.filter(pk=1).update(whatsapp_url="https://wa.me/")
    PersonalityItem.objects.filter(label_ru__in=HIDE_RU).update(is_active=True)
    PersonalityItem.objects.filter(label_en__in=HIDE_EN).update(is_active=True)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_cms_section_verbose_names"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="phone",
            field=models.CharField(
                blank=True,
                default="+380 95 472 7859",
                max_length=64,
                verbose_name="Телефон",
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="whatsapp_url",
            field=models.URLField(
                blank=True,
                default="https://wa.me/qr/ZPQAL5UEFCQIN1",
                verbose_name="WhatsApp",
            ),
        ),
        migrations.RunPython(apply_site_content, revert_site_content),
    ]
