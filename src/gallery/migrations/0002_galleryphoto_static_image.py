# Generated manually for static_image (Vercel-safe gallery)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gallery", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="galleryphoto",
            name="static_image",
            field=models.CharField(
                blank=True,
                help_text="Шлях у static/, напр. images/gallery/gallery-01.jpg (Vercel-safe)",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="galleryphoto",
            name="image",
            field=models.ImageField(blank=True, upload_to="gallery/"),
        ),
    ]
