from django.contrib import admin

# Register your models here.

from .models import GalleryPhoto, Volunteer

@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

admin.site.register(Volunteer)