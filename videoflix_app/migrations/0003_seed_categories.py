
from django.db import migrations

DEFAULT_CATEGORIES = [
    "Action", "Comedy", "Drama", "Horror", "Sci-Fi",
    "Documentary", "Animation", "Thriller", "Romance",
    "Adventure", "Fantasy", "Mystery", "Crime",
    "Musical", "War", "Western", "Other"
]


def seed_categories(apps, schema_editor):
    Category = apps.get_model('videoflix_app', 'Category')
    for name in DEFAULT_CATEGORIES:
        Category.objects.get_or_create(name=name)


def reverse_seed(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('videoflix_app', '0002_rename_descripition_video_description.py'),  # <-- anpassen!
    ]

    operations = [
        migrations.RunPython(seed_categories, reverse_seed),
    ]