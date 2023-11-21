from django.contrib import admin
from .models import SelfMailModel, HeaderAndFooter, Newsletter, FileModel
# Register your models here.

admin.site.register(SelfMailModel)

class HeaderAndFoooterAdmin(admin.ModelAdmin):
    readonly_fields = ('header_image_url', 'footer_image_url')
admin.site.register(HeaderAndFooter, HeaderAndFoooterAdmin) 
admin.site.register(FileModel)
admin.site.register(Newsletter)
