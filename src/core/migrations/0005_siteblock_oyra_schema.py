from django.db import migrations, models


IMAGE_KEYS = frozenset(
    {
        "hero.media",
        "about.portrait",
        "personality.portrait",
        "contacts.bg",
    }
)


def forwards_siteblock_schema(apps, schema_editor):
    SiteBlock = apps.get_model("core", "SiteBlock")
    for block in SiteBlock.objects.all().iterator():
        block.is_active = bool(getattr(block, "is_visible", True))
        if block.key.endswith("_section_visible") or block.key.endswith("_visible"):
            on = bool(getattr(block, "is_visible", True))
            if block.text_ru.strip() not in {"0", "1", "true", "True", "false", "False"}:
                block.text_ru = "1" if on else "0"
                block.text_en = block.text_ru
            elif block.text_ru.strip() in {"false", "False", "0"}:
                block.text_ru = "0"
                block.text_en = "0"
            else:
                block.text_ru = "1"
                block.text_en = "1"
            block.is_active = True
        block.content_type = "image" if block.key in IMAGE_KEYS else "text"
        block.sort_order = block.sort_order or 0
        block.save(
            update_fields=[
                "is_active",
                "text_ru",
                "text_en",
                "content_type",
                "sort_order",
            ]
        )


def backwards_siteblock_schema(apps, schema_editor):
    SiteBlock = apps.get_model("core", "SiteBlock")
    for block in SiteBlock.objects.all().iterator():
        if block.key.endswith("_section_visible") or block.key.endswith("_visible"):
            block.is_visible = block.text_ru.strip() in {"1", "true", "True"}
        else:
            block.is_visible = bool(block.is_active)
        block.save(update_fields=["is_visible"])


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_section_style_and_chrome_proxies"),
    ]

    operations = [
        migrations.AddField(
            model_name="siteblock",
            name="content_type",
            field=models.CharField(
                choices=[("text", "Текст"), ("image", "Фото")],
                default="text",
                max_length=16,
                verbose_name="Тип контента",
            ),
        ),
        migrations.AddField(
            model_name="siteblock",
            name="sort_order",
            field=models.PositiveSmallIntegerField(default=0, verbose_name="Порядок"),
        ),
        migrations.AddField(
            model_name="siteblock",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Активен"),
        ),
        migrations.RunPython(forwards_siteblock_schema, backwards_siteblock_schema),
        migrations.RemoveField(
            model_name="siteblock",
            name="is_visible",
        ),
        migrations.AlterModelOptions(
            name="siteblock",
            options={
                "ordering": ["page", "sort_order", "key"],
                "verbose_name": "Блок контента",
                "verbose_name_plural": "Блоки контента",
            },
        ),
        migrations.AlterField(
            model_name="siteblock",
            name="image",
            field=models.ImageField(
                blank=True, upload_to="blocks/", verbose_name="Изображение"
            ),
        ),
        migrations.AlterField(
            model_name="siteblock",
            name="key",
            field=models.CharField(max_length=64, verbose_name="Ключ блока"),
        ),
        migrations.AlterField(
            model_name="siteblock",
            name="label",
            field=models.CharField(
                blank=True, max_length=128, verbose_name="Название в админке"
            ),
        ),
        migrations.AlterField(
            model_name="siteblock",
            name="page",
            field=models.CharField(
                choices=[
                    ("home", "Главная"),
                    ("privacy", "Политика"),
                    ("site", "Сайт"),
                ],
                max_length=32,
                verbose_name="Страница",
            ),
        ),
        migrations.AlterField(
            model_name="siteblock",
            name="text_en",
            field=models.TextField(blank=True, verbose_name="Текст EN"),
        ),
        migrations.AlterField(
            model_name="siteblock",
            name="text_ru",
            field=models.TextField(blank=True, verbose_name="Текст RU"),
        ),
        migrations.AlterModelOptions(
            name="homeaboutsettings",
            options={
                "verbose_name": "Главная — Обо мне",
                "verbose_name_plural": "Главная — Обо мне",
            },
        ),
        migrations.AlterModelOptions(
            name="homecontactssettings",
            options={
                "verbose_name": "Главная — Контакты",
                "verbose_name_plural": "Главная — Контакты",
            },
        ),
        migrations.AlterModelOptions(
            name="homefaqsettings",
            options={
                "verbose_name": "Главная — Вопросы",
                "verbose_name_plural": "Главная — Вопросы",
            },
        ),
        migrations.AlterModelOptions(
            name="homeformatssettings",
            options={
                "verbose_name": "Главная — Форматы",
                "verbose_name_plural": "Главная — Форматы",
            },
        ),
        migrations.AlterModelOptions(
            name="homegallerysettings",
            options={
                "verbose_name": "Главная — Галерея",
                "verbose_name_plural": "Главная — Галерея",
            },
        ),
        migrations.AlterModelOptions(
            name="homeherosettings",
            options={
                "verbose_name": "Главная — Hero",
                "verbose_name_plural": "Главная — Hero",
            },
        ),
        migrations.AlterModelOptions(
            name="homepersonalitysettings",
            options={
                "verbose_name": "Главная — Личность",
                "verbose_name_plural": "Главная — Личность",
            },
        ),
        migrations.AlterModelOptions(
            name="hometestimonialssettings",
            options={
                "verbose_name": "Главная — Отзывы",
                "verbose_name_plural": "Главная — Отзывы",
            },
        ),
        migrations.AlterModelOptions(
            name="privacysettings",
            options={
                "verbose_name": "Политика конфиденциальности",
                "verbose_name_plural": "Политика конфиденциальности",
            },
        ),
        migrations.AlterModelOptions(
            name="siteerrorssettings",
            options={
                "verbose_name": "Страницы ошибок",
                "verbose_name_plural": "Страницы ошибок",
            },
        ),
        migrations.AlterModelOptions(
            name="sitefootersettings",
            options={"verbose_name": "Подвал", "verbose_name_plural": "Подвал"},
        ),
        migrations.AlterModelOptions(
            name="siteuisettings",
            options={
                "verbose_name": "Интерфейс и формы",
                "verbose_name_plural": "Интерфейс и формы",
            },
        ),
        migrations.AlterModelOptions(
            name="themestylessettings",
            options={"verbose_name": "Стили", "verbose_name_plural": "Стили"},
        ),
    ]
