from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_education"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="tech_stack",
            field=models.CharField(default="Belum diisi", max_length=255),
        ),
    ]
