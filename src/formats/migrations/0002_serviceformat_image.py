from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("formats", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="serviceformat",
            name="image",
            field=models.ImageField(blank=True, upload_to="formats/"),
        ),
    ]
