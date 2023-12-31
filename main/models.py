from django.db import models
from autoslug import AutoSlugField


class Property(models.Model):
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        
    address = models.TextField()
    slug = AutoSlugField(populate_from='address', unique_with=['state_code', 'postal_code'])
    source_url = models.URLField(max_length=200)
    agent = models.ForeignKey('main.Agent', null=True, blank=True, on_delete=models.CASCADE)
    primary_photo = models.URLField(max_length=200, null=True, blank=True)
    neighborhood = models.ForeignKey('main.Neighborhood', null=True, blank=True, on_delete=models.CASCADE)
    flood_factor_severity = models.CharField(max_length=20, null=True, blank=True)
    flood_trend = models.CharField(max_length=200, null=True, blank=True)
    fire_factor_severity = models.CharField(max_length=20, null=True, blank=True)
    fire_trend = models.CharField(max_length=200, null=True, blank=True)
    noice_score = models.CharField(max_length=20, null=True, blank=True)
    flood_trend = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)
    coming_soon_date = models.DateTimeField(null=True, blank=True)
    list_price = models.IntegerField(null=True, blank=True)
    list_price_min = models.IntegerField(null=True, blank=True)
    list_price_max = models.IntegerField(null=True, blank=True)
    last_price_change_amount = models.IntegerField(null=True, blank=True)
    last_sold_date = models.DateTimeField(null=True, blank=True)
    last_sold_price = models.IntegerField(null=True, blank=True)
    price_per_sqft = models.IntegerField(null=True, blank=True)
    list_date = models.DateTimeField(null=True, blank=True)
    nearby_schools = models.ManyToManyField('main.School', related_name='properties')
    waterfront_water_access = models.ManyToManyField('main.ListItem', related_name='waterfront_water_access_item')
    land_info = models.ManyToManyField('main.ListItem', related_name='land_info_item')
    school_information = models.ManyToManyField('main.ListItem', related_name='school_info_item')
    hoa = models.ManyToManyField('main.ListItem', related_name='hoa_item')
    other_property_info = models.ManyToManyField('main.ListItem', related_name='property_info_item')
    utilities = models.ManyToManyField('main.ListItem', related_name='utility')
    street_view_url = models.URLField(max_length=400, null=True, blank=True)
    street_view_metadata_url = models.URLField(max_length=400, null=True, blank=True)
    street_number = models.CharField(max_length=20, null=True, blank=True)
    street_direction = models.CharField(max_length=20, null=True, blank=True)
    street_name = models.CharField(max_length=100, null=True, blank=True)
    street_suffix = models.CharField(max_length=20, null=True, blank=True)
    street_post_direction = models.CharField(max_length=20, null=True, blank=True)
    unit = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state_code = models.CharField(max_length=5, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    county = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.DecimalField(decimal_places=6, max_digits=10, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=6, max_digits=10, null=True, blank=True)
    driving_directions = models.CharField(max_length=20, null=True, blank=True)
    builder = models.CharField(max_length=20, null=True, blank=True)
    tags = models.ManyToManyField('main.ListItem', related_name="tag")
    unit_count = models.IntegerField(null=True, blank=True)
    baths = models.IntegerField(null=True, blank=True)
    baths_min = models.IntegerField(null=True, blank=True)
    baths_max = models.IntegerField(null=True, blank=True)
    baths_consolidated = models.CharField(max_length=5, null=True, blank=True)
    baths_full = models.IntegerField(null=True, blank=True)
    baths_3qtr = models.IntegerField(null=True, blank=True)
    baths_half = models.IntegerField(null=True, blank=True)
    baths_total = models.IntegerField(null=True, blank=True)
    beds = models.IntegerField(null=True, blank=True)
    beds_min = models.IntegerField(null=True, blank=True)
    beds_max = models.IntegerField(null=True, blank=True)
    garage = models.IntegerField(null=True, blank=True)
    garage_min = models.IntegerField(null=True, blank=True)
    garage_max = models.IntegerField(null=True, blank=True)
    garage_type = models.CharField(max_length=50, null=True, blank=True)
    construction = models.CharField(max_length=50, null=True, blank=True)
    cooling = models.CharField(max_length=50, null=True, blank=True)
    exterior = models.CharField(max_length=50, null=True, blank=True)
    fireplace = models.CharField(max_length=50, null=True, blank=True)
    heating = models.CharField(max_length=20, null=True, blank=True)
    roofing = models.CharField(max_length=20, null=True, blank=True)
    pool = models.CharField(max_length=20, null=True, blank=True)
    sqft = models.IntegerField(null=True, blank=True)
    sqft_min = models.IntegerField(null=True, blank=True)
    sqft_max = models.IntegerField(null=True, blank=True)
    lot_sqft = models.IntegerField(null=True, blank=True)
    rooms = models.IntegerField(null=True, blank=True)
    stories = models.IntegerField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)
    sub_type = models.CharField(max_length=20, null=True, blank=True)
    units = models.IntegerField(null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)
    year_renovated = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    zoning = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.slug
    
    def photos_count(self):
        return self.photos.count()


class ListItem(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Flags(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='flags')
    is_pending = models.BooleanField(null=True)
    is_contingent = models.BooleanField(null=True)
    is_new_listing = models.BooleanField(null=True)
    is_new_construction = models.BooleanField(null=True)
    is_short_sale = models.BooleanField(null=True)
    is_foreclosure = models.BooleanField(null=True)
    is_price_reduced = models.BooleanField(null=True)
    is_senior_community = models.BooleanField(null=True)
    is_deal_available = models.BooleanField(null=True)
    is_price_excludes_land = models.BooleanField(null=True)
    is_subdivision = models.BooleanField(null=True)
    is_coming_soon = models.BooleanField(null=True)
    is_for_rent = models.BooleanField(null=True)
    is_garage_present = models.BooleanField(null=True)
    
    def __str__(self):
        return f"Flag: {self.property.slug}"

class Neighborhood(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    slug_id = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='slug_id', unique_with=['id'])
    median_listing_price = models.IntegerField(null=True, blank=True)
    nearby_neighborhoods = models.ManyToManyField('main.Neighborhood')
    state_code = models.CharField(max_length=5, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return self.local_url
    
    def properties(self):
        return self.property_set.all()
    
    def properties_count(self):
        return self.property_set.count()

class PriceHistory(models.Model):
    property = models.ForeignKey(Property, null=True, on_delete=models.CASCADE, related_name='price_history')
    date = models.DateField()
    event = models.CharField(max_length=20)
    price = models.IntegerField()
    price_sqft = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=20)

    def __str__(self):
        return f"PriceHistory: {self.property.name}"
class TaxHistory(models.Model):
    property = models.ForeignKey(Property, null=True, on_delete=models.CASCADE, related_name='tax_history')
    year = models.IntegerField()
    tax = models.IntegerField()
    land = models.IntegerField()
    building = models.IntegerField(null=True, blank=True)
    total = models.IntegerField()

    def __str__(self):
        return f"TaxHistory: {self.year}"    

class School(models.Model):
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='name', unique_with=['id'])
    latitude = models.DecimalField(decimal_places=6, max_digits=10, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=6, max_digits=10, null=True, blank=True)
    education_levels = models.ManyToManyField('main.ListItem', related_name='level')
    district = models.CharField(max_length=50, null=True, blank=True)
    greatschools_id = models.CharField(max_length=20, null=True, blank=True)
    nces_code = models.CharField(max_length=20, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    grades = models.ManyToManyField('main.ListItem', related_name='grade')
    funding_type = models.CharField(max_length=10, null=True, blank=True)
    student_count = models.IntegerField(null=True, blank=True)
    review_count = models.IntegerField(null=True, blank=True)
    parent_rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def nearby_properties(self):
        return self.properties.all()
    
    def nearby_properties_count(self):
        return self.properties.count()
    

class Agent(models.Model):
    agent_id = models.CharField(max_length=20)
    slug = AutoSlugField(populate_from='agent_id', unique_with=['id'])
    city = models.CharField(max_length=20, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    state_code = models.CharField(max_length=5, null=True, blank=True)
    country = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    phones = models.ManyToManyField('main.ListItem', related_name='phone')
    description = models.TextField(null=True, blank=True)
    specializations = models.ManyToManyField('main.ListItem', related_name='specialization')
    zips = models.ManyToManyField('main.ListItem', related_name='zip')
    website = models.URLField(max_length=200, null=True, blank=True)
    broker = models.CharField(max_length=50, null=True, blank=True)
    broker_address = models.CharField(max_length=20, null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.agent_id
    
    def properties(self):
        return self.property_set.all()
    
    def properties_count(self):
        return self.property_set.count()
    

class ServedAreas(models.Model):
    name = models.CharField(max_length=20)
    state_code = models.CharField(max_length=5)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Image(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='photos')
    image = models.URLField(max_length=200)
    
    def __str__(self):
        return '{} - {}'.format(self.property.slug, self.image)

class ImageTag(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='tags')
    label = models.CharField(max_length=20)
    probability = models.DecimalField(decimal_places=15, max_digits=25, null=True, blank=True)