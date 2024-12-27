from django.contrib import admin

from main.models import InfoOnPage


@admin.register(InfoOnPage)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ("page_name",)