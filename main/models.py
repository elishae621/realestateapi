from django.db import models
from autoslug import AutoSlugField


# Property is grouped into the following:
# Property information
# location information
# price infromation
# details
# features 
# environmental factors 
# agent & broker

class Property(models.Model):
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        
    address = models.TextField(null=True, blank=True)
    slug = AutoSlugField(populate_from='address', unique_with=['pk'])
    source_url = models.URLField(max_length=200, null=True, blank=True)
    agent = models.ForeignKey('main.Agent', null=True, blank=True, on_delete=models.CASCADE)
    primary_photo = models.URLField(max_length=200, null=True, blank=True)
    Neighborhood = models.ForeignKey('main.Neighborhood', null=True, blank=True, on_delete=models.CASCADE)
    flood_factor_severity = models.CharField(max_length=20, null=True, blank=True)
    flood_trend = models.CharField(max_length=200, null=True, blank=True)
    fire_factor_severity = models.CharField(max_length=20, null=True, blank=True)
    fire_trend = models.CharField(max_length=200, null=True, blank=True)
    noice_score = models.CharField(max_length=20, null=True, blank=True)
    flood_trend = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)
    coming_soon_date = models.DateTimeField(null=True, blank=True)
    list_price = models.IntegerField(null=True, blank=True)
    list_price_change_amount = models.IntegerField(null=True, blank=True)
    last_sold_date = models.DateTimeField(null=True, blank=True)
    last_sold_price = models.IntegerField(null=True, blank=True)
    price_per_sqft = models.IntegerField(null=True, blank=True)
    list_date = models.DateTimeField(null=True, blank=True)
    schools = models.ManyToManyField('main.School', verbose_name="Nearby Schools")
    waterfront_water_access = models.ManyToManyField('main.ListItem', related_name='waterfront_water_access_item')
    land_info = models.ManyToManyField('main.ListItem', related_name='land_info_item')
    school_information = models.ManyToManyField('main.ListItem', related_name='school_info_item')
    hoa = models.ManyToManyField('main.ListItem', related_name='hoa_item')
    other_property_info = models.ManyToManyField('main.ListItem', related_name='property_info_item')
    utilities = models.ManyToManyField('main.ListItem', related_name='utility')
    street_view_url = models.URLField(max_length=400, null=True, blank=True)
    street_view_metadata_url = models.URLField(max_length=400, null=True, blank=True)
    street_number = models.CharField(max_length=20, null=True, blank=True),
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
    validation_code = models.CharField(max_length=10, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.DecimalField(decimal_places=6, max_digits=10, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=6, max_digits=10, null=True, blank=True)
    driving_directions = models.CharField(max_length=20, null=True, blank=True)
    builder = models.CharField(max_length=20, null=True, blank=True)
    tags = models.ManyToManyField('main.ListItem', related_name="tag")
    unit_count = models.IntegerField(null=True, blank=True)
    baths = models.IntegerField(null=True, blank=True)
    baths_consolidated = models.IntegerField(null=True, blank=True)
    baths_full = models.IntegerField(null=True, blank=True)
    baths_3qtr = models.IntegerField(null=True, blank=True)
    baths_half = models.IntegerField(null=True, blank=True)
    baths_total = models.IntegerField(null=True, blank=True)
    beds = models.IntegerField(null=True, blank=True)
    garage = models.CharField(max_length=50, null=True, blank=True)
    garage_type = models.CharField(max_length=50, null=True, blank=True)
    construction = models.CharField(max_length=50, null=True, blank=True)
    cooling = models.CharField(max_length=50, null=True, blank=True)
    exterior = models.CharField(max_length=50, null=True, blank=True)
    fireplace = models.CharField(max_length=50, null=True, blank=True)
    heating = models.CharField(max_length=20, null=True, blank=True)
    roofing = models.CharField(max_length=20, null=True, blank=True)
    garage = models.CharField(max_length=20, null=True, blank=True)
    garage = models.CharField(max_length=20, null=True, blank=True)
    pool = models.CharField(max_length=20, null=True, blank=True)
    sqft = models.IntegerField(null=True, blank=True)
    lot_sqft = models.IntegerField(null=True, blank=True)
    rooms = models.IntegerField(null=True, blank=True)
    stories = models.IntegerField(null=True, blank=True)
    sub_type = models.CharField(max_length=20, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)
    units = models.IntegerField(null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)
    year_renovated = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    zoning = models.CharField(max_length=50, null=True, blank=True)
    primary_photo = models.URLField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.slug


class ListItem(models.Model):
    name = models.CharField(max_length=200)

class Flags(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
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

class Neighborhood(models.Model):
    area = models.CharField(max_length=50, null=True, blank=True)
    local_url = models.CharField(max_length=50, null=True, blank=True, unique=True)
    median_listing_price = models.IntegerField(null=True, blank=True)
    median_sold_price = models.IntegerField(null=True, blank=True)
    median_days_on_market = models.IntegerField(null=True, blank=True)
    median_price_per_sqft = models.IntegerField(null=True, blank=True)
    nearby_neighborhoods = models.ManyToManyField('main.Neighborhood')
    

class PriceHistory(models.Model):
    property = models.ForeignKey(Property, null=True, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    event = models.CharField(max_length=20, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    price_sqft = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=20, null=True, blank=True)

class TaxHistory(models.Model):
    property = models.ForeignKey(Property, null=True, on_delete=models.CASCADE)
    year = models.IntegerField(null=True, blank=True)
    taxes = models.IntegerField(null=True, blank=True)
    land = models.IntegerField(null=True, blank=True)
    additions = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)

class School(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.DecimalField(decimal_places=6, max_digits=10, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=6, max_digits=10, null=True, blank=True)
    education_levels = models.ManyToManyField('main.ListItem', related_name='level')
    distance_in_miles = models.DecimalField(decimal_places=1, max_digits=4, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    greatschools_id = models.CharField(max_length=20, null=True, blank=True)
    nces_code = models.CharField(max_length=20, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    grades = models.ManyToManyField('main.ListItem', related_name='grade')
    funding_type = models.CharField(max_length=10, null=True, blank=True)
    student_count = models.IntegerField(null=True, blank=True)
    review_count = models.IntegerField(null=True, blank=True)
    parent_rating = models.IntegerField(null=True, blank=True)


class Agent(models.Model):
    agent_id = models.CharField(max_length=20, null=True, blank=True, unique=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    state_code = models.CharField(max_length=5, null=True, blank=True)
    country = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    phones = models.ManyToManyField('main.ListItem', related_name='phone')
    description = models.TextField(null=True, blank=True)
    specializations = models.ManyToManyField('main.ListItem', related_name='specialization')
    languages = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    broker = models.CharField(max_length=50, null=True, blank=True)
    broker_address = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    
class ServedAreas(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    state_code = models.CharField(max_length=5, null=True, blank=True)
    agent = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.CASCADE)

class Image(models.Model):
    property = models.ForeignKey(Property, null=True, blank=True, on_delete=models.CASCADE)
    image = models.URLField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return '{} - {}'.format(self.property.slug, self.image)

class ImageTag(models.Model):
    image = models.ForeignKey(Image, null=True, blank=True, on_delete=models.CASCADE)
    label = models.CharField(max_length=20, null=True, blank=True)
    probability = models.DecimalField(decimal_places=20, max_digits=25, null=True, blank=True)