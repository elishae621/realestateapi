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
    slug = AutoSlugField(populate_from='address', unique_with=['pk',],)
    source_url = models.URLField(max_length=200)
    agent = models.ForeignKey('main.Agent', null=True, on_delete=models.CASCADE)
    Neighborhood = models.ForeignKey('main.Neighborhood', null=True, on_delete=models.CASCADE)
    flood_factor_score = models.IntegerField()
    flood_fema_zone = models.CharField(max_length=5)
    move_in_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10)
    coming_soon_date = models.DateTimeField(null=True, blank=True)
    list_price = models.IntegerField()
    list_price_change_amount = models.IntegerField()
    list_price_min = models.IntegerField()
    list_price_max = models.IntegerField()
    price_per_sqft = models.IntegerField()
    list_date = models.DateTimeField(null=True, blank=True)
    schools = models.ManyToManyField('main.School', verbose_name="Nearby Schools")
    waterfront_water_access = models.ManyToManyField('main.ListItem', related_name='waterfront_water_access_item')
    land_info = models.ManyToManyField('main.ListItem', related_name='land_info_item')
    school_information = models.ManyToManyField('main.ListItem', related_name='school_info_item')
    hoa = models.ManyToManyField('main.ListItem', related_name='hoa_item')
    other_property_info = models.ManyToManyField('main.ListItem', related_name='property_info_item')
    utilities = models.ManyToManyField('main.ListItem', related_name='utility')
    street_view_url = models.URLField(max_length=400)
    street_view_metadata_url = models.URLField(max_length=400)
    street_number = models.CharField(max_length=20),
    street_direction = models.CharField(max_length=20)
    street_name = models.CharField(max_length=100)
    street_suffix = models.CharField(max_length=20)
    street_post_direction = models.CharField(max_length=20)
    unit = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state_code = models.CharField(max_length=5)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=20)
    validation_code = models.CharField(max_length=10)
    state = models.CharField(max_length=20)
    lat = models.DecimalField(decimal_places=6, max_digits=10)
    lon = models.DecimalField(decimal_places=6, max_digits=10)
    county = models.CharField(max_length=20)
    cross_street = models.CharField(max_length=20)
    driving_directions = models.CharField(max_length=20)
    builder = models.CharField(max_length=20)
    tags = models.ManyToManyField('main.ListItem', related_name="tag")
    unit_count = models.IntegerField()
    baths = models.IntegerField()
    baths_consolidated = models.IntegerField()
    baths_full = models.IntegerField()
    baths_3qtr = models.IntegerField()
    baths_half = models.IntegerField()
    baths_1qtr = models.IntegerField()
    baths_min = models.IntegerField()
    baths_max = models.IntegerField()
    beds_min = models.IntegerField()
    beds_max = models.IntegerField()
    beds = models.IntegerField()
    garage = models.CharField(max_length=20)
    pool = models.CharField(max_length=20)
    sqft = models.IntegerField()
    sqft_min = models.IntegerField()
    sqft_max = models.IntegerField()
    lot_sqft = models.IntegerField()
    rooms = models.IntegerField()
    stories = models.IntegerField()
    sub_type = models.CharField(max_length=20)
    text = models.TextField()
    type = models.CharField(max_length=20)
    units = models.IntegerField()
    unit_type = models.CharField(max_length=20)
    year_built = models.IntegerField()
    name = models.CharField(max_length=50)
    
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
    name = models.CharField(max_length=50)
    median_listing_price = models.IntegerField()
    median_sold_price = models.IntegerField()
    median_days_on_market = models.IntegerField()
    median_rental_price = models.IntegerField()
    median_listing_price_per_sqft = models.IntegerField()
    popular_searches = models.TextField()
    nearby_neighborhoods = models.ManyToManyField('main.Neighborhood')
    

class FloorPlan(models.Model):
    
    # def image_location(self, filename):
    #     format = filename.split('.')[1]
    #     filename = generate_filename() + '.' + format
    #     return '/'.join(['floorplan/', self.property.country,
    #                      self.property.state,
    #                      self.property.county, self.property.s[:20] + str(randnum), filename])

    property = models.ForeignKey(Property, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    availability = models.CharField(max_length=20)
    beds = models.IntegerField()
    baths = models.IntegerField()
    area = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField()

class PriceHistory(models.Model):
    property = models.ForeignKey(Property, null=True, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    event = models.CharField(max_length=20)
    price = models.IntegerField()
    price_sqft = models.IntegerField()
    source = models.CharField(max_length=20)
    
class TaxHistory(models.Model):
    property = models.ForeignKey(Property, null=True, on_delete=models.CASCADE)
    year = models.IntegerField()
    taxes = models.IntegerField()
    land = models.IntegerField()
    additions = models.IntegerField()
    total = models.IntegerField()

class School(models.Model):
    name = models.CharField(max_length=50)
    education_levels = models.ManyToManyField('main.ListItem', related_name='level')
    distance_in_miles = models.DecimalField(decimal_places=1, max_digits=4)
    student_teacher_ratio = models.DecimalField(decimal_places=1, max_digits=4)
    rating = models.IntegerField()
    grades = models.ManyToManyField('main.ListItem', related_name='grade')
    funding_type = models.CharField(max_length=10)
    student_count = models.IntegerField()
    review_count = models.IntegerField()
    parent_rating = models.IntegerField()
    assigned = models.BooleanField(null=True)


class Agent(models.Model):
    agent_id = models.CharField(max_length=20, unique=True)
    atype = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    brokerage = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    about = models.TextField()
    experience = models.CharField(max_length=20)
    areas_served = models.TextField()
    specializations = models.TextField()
    languages = models.CharField(max_length=50)
    website = models.URLField(max_length=200)
    brokerage = models.CharField(max_length=50)
    broker_phone = models.CharField(max_length=20)
    broker_adddress = models.CharField(max_length=20)
    broker_website = models.URLField(max_length=200)

class Image(models.Model):
    property = models.ForeignKey(Property, blank=True, on_delete=models.CASCADE)
    url = models.URLField(max_length=200)
    
    def __str__(self):
        return '{} - {}'.format(self.property.slug, self.url)
    
class ImageTag(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    label = models.CharField(max_length=20)
    probability = models.DecimalField(decimal_places=20, max_digits=25)