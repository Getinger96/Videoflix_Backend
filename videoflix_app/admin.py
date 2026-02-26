from django.contrib import admin
from django.db import models
from .models import Category, Video
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django import forms

# Register your models here#

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



