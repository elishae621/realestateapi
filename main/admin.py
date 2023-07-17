from django.contrib import admin
from main import models


class FlagsAdmin(admin.StackedInline):
    model = models.Flags
    

class PriceHistoryAdmin(admin.StackedInline):
    model = models.PriceHistory
    

class TaxHistoryAdmin(admin.StackedInline):
    model = models.TaxHistory
    
class ServedAreasAdmin(admin.StackedInline):
    model = models.ServedAreas

class ImageAdmin(admin.StackedInline):
    model = models.Image

class ImageTagAdmin(admin.StackedInline):
    model = models.ImageTag
    
@admin.register(models.Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('slug', 'source_url')
    inlines = [FlagsAdmin, PriceHistoryAdmin, TaxHistoryAdmin, ImageAdmin]


@admin.register(models.Image)
class ImageMainAdmin(admin.ModelAdmin):
    inlines = [ImageTagAdmin,]

@admin.register(models.Agent)
class AgentAdmin(admin.ModelAdmin):
    inlines = [ServedAreasAdmin,]
