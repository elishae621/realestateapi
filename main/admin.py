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
    


@admin.register(models.Image)
class ImageMainAdmin(admin.ModelAdmin):
    inlines = [ImageTagAdmin,]

@admin.register(models.Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('slug', 'source_url')
    readonly_fields = ('slug',)
    list_filter = ('state_code',)
    search_fields = ('slug', 'address', 'state',)
    inlines = [FlagsAdmin, PriceHistoryAdmin, TaxHistoryAdmin, ImageAdmin]

@admin.register(models.Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('slug', 'properties_count')
    readonly_fields = ('slug', 'properties_count')
    list_filter = ('state_code',)
    search_fields = ('slug',)
    inlines = [ServedAreasAdmin,]

@admin.register(models.School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('slug', 'nearby_properties_count')
    search_fields = ('slug',)
    readonly_fields = ('slug', 'nearby_properties')

@admin.register(models.Neighborhood)
class NeighborhoodAdmin(admin.ModelAdmin):
    list_display = ('slug', 'local_url',)
    search_fields = ('slug',)
    readonly_fields = ('nearby_neighborhoods',)