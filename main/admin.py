from django.contrib import admin
from main import models


class FlagsAdmin(admin.StackedInline):
    model = models.Flags
    extra = 0
    

class PriceHistoryAdmin(admin.StackedInline):
    model = models.PriceHistory
    extra = 0
    

class TaxHistoryAdmin(admin.StackedInline):
    model = models.TaxHistory
    extra = 0
    

class ServedAreasAdmin(admin.StackedInline):
    model = models.ServedAreas
    extra = 0


class ImageAdmin(admin.StackedInline):
    model = models.Image
    extra = 0


class ImageTagAdmin(admin.StackedInline):
    model = models.ImageTag
    extra = 0
    

@admin.register(models.Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('slug', 'source_url')
    inlines = [FlagsAdmin, PriceHistoryAdmin, TaxHistoryAdmin, ImageAdmin]


@admin.register(models.Image)
class ImageMainAdmin(admin.ModelAdmin):
    inlines = [ImageTagAdmin,]
    extra = 0


@admin.register(models.Agent)
class AgentAdmin(admin.ModelAdmin):
    inlines = [ServedAreasAdmin,]
    extra = 0
