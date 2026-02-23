from django.contrib import admin
from .models import Video
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here#

#https://stackoverflow.com/questions/12626171/django-admin-choice-field

class VideoResource(resources.ModelResource):

    class Meta:
        model = Video

@admin.register(Video)

class VideoAdmin(ImportExportModelAdmin):
    list_display = ['title', 'descripition','category']
    resource_class = VideoResource
