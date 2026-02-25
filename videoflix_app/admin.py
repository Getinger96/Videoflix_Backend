from django.contrib import admin
from django.db import models
from .models import Category, Video
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django import forms

# Register your models here#

#https://stackoverflow.com/questions/12626171/django-admin-choice-field


class VideoResource(resources.ModelResource):

    class Meta:
        model = Video

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']



@admin.register(Video)

class VideoAdmin(ImportExportModelAdmin):
    list_display = ['title', 'description','category']
    resource_class = VideoResource



# from videoflix_app.models import Category

# default_categories = [
#     'Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi',
#     'Documentary', 'Animation', 'Thriller', 'Romance',
#     'Adventure', 'Fantasy', 'Mystery', 'Crime',
#     'Musical', 'War', 'Western', 'Other'
# ]

# for name in default_categories:
#     Category.objects.get_or_create(name=name)

# print("Standard-Kategorien erstellt!")