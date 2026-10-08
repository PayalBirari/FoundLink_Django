from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0010_alter_founditem_image_alter_lostitem_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="founditem",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="found_items/",
            ),
        ),
        migrations.AlterField(
            model_name="lostitem",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="lost_items/",
            ),
        ),
    ]