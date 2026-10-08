from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_company_legal_and_address"),
    ]

    operations = [
        migrations.CreateModel(
            name="TermsSettings",
            fields=[],
            options={
                "verbose_name": "Условия использования",
                "verbose_name_plural": "Условия использования",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.sitesettings",),
        ),
        migrations.AlterField(
            model_name="siteblock",
            name="page",
            field=models.CharField(
                choices=[
                    ("home", "Главная"),
                    ("privacy", "Политика"),
                    ("terms", "Условия"),
                    ("site", "Сайт"),
                ],
                max_length=32,
                verbose_name="Страница",
            ),
        ),
    ]
