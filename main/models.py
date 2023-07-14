from django.db import models
from autoslug import AutoSlugField
import uuid
import random

def generate_filename():
    return str(uuid.uuid4())[-3:].upper() + '-' + str(random.randint(1, 1000))

randnum = str(random.randint(1, 100))

class PaymentFrequency(models.TextChoices):
    OneTime = ''
    YEARLY = 'YEARLY'
    MONTHLY = 'MONTHLY'
    WEEKLY = 'WEEKLY'
    DAILY = 'DAILY'


class Category(models.TextChoices):
    RENT = 'RENT'
    SALE = 'SALE'

class Property(models.Model):
    address = models.TextField(null=True, blank=True)
    slug = AutoSlugField(populate_from='address', unique_with=['pk',],)
    price = models.IntegerField()
    price_per_sqft = models.IntegerField()
    monthly_payment = models.IntegerField()
    category = models.CharField(choices=Category.choices, max_length=10)
    author = models.ForeignKey('main.Agent', null=True, on_delete=models.CASCADE)
    bedrooms = models.CharField(max_length=200)
    bathrooms = models.CharField(max_length=200)
    other_rooms = models.CharField(max_length=200)
    studio = models.BooleanField()
    interior_features = models.TextField()
    kitchen_and_dinning = models.TextField()
    appliances = models.TextField()
    area = models.IntegerField(null=True, blank=True, help_text="in sqft")
    neighborhood = models.CharField(max_length=20)
    area = models.CharField(max_length=200)
    lot_sqft = models.IntegerField()
    county = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    property_type = models.CharField(max_length=30)
    property_subtype = models.CharField(max_length=30)
    last_updated = models.DateTimeField(auto_now=True)
    pets_allowed = models.BooleanField()
    pets_features = models.BooleanField()
    year_built = models.PositiveIntegerField(null=True, blank=True)
    availablity = models.DateField(null=True, blank=True)
    about = models.TextField()
    heating_and_cooling = models.TextField()
    garage_and_parking = models.TextField()
    homeowners_association = models.TextField()
    hoa_fees = models.TextField()
    school_information = models.TextField()
    property_info = models.TextField()
    building_and_construction = models.TextField()
    land_info = models.TextField()
    utilities = models.TextField()
    manufactured_and_mobile_info = models.TextField()
    home_features = models.TextField()
    amenities = models.TextField()
    features = models.TextField()
    one_time_fees = models.TextField()
    one_time_fees = models.TextField()
    recurring_fees = models.TextField()
    lease_terms = models.TextField()
    
    flood_factor = models.CharField(max_length=20)
    fire_factor = models.CharField(max_length=20)
    schools = models.ManyToManyField('main.School', verbose_name="Nearby Schools")
    schools = models.ManyToManyField('main.Property', verbose_name="Nearby Properties")
    data_source = models.CharField(max_length=50)
    data_source_copyright = models.CharField(max_length=50)
    


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
    
    def image_location(self, filename):
        format = filename.split('.')[1]
        filename = generate_filename() + '.' + format
        return '/'.join(['floorplan/', self.property.country,
                         self.property.state,
                         self.property.county, self.property.s[:20] + str(randnum), filename])

    property = models.ForeignKey(Property, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    availability = models.CharField(max_length=20)
    beds = models.IntegerField()
    baths = models.IntegerField()
    area = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField()

class PropertyPriceHistory(models.Model):
    property = models.ForeignKey(Property, null=True, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    event = models.CharField(max_length=20)
    price = models.IntegerField()
    price_per_sqft = models.IntegerField()
    source = models.CharField(max_length=20)
    
class PropertyTaxHistory(models.Model):
    property = models.ForeignKey(Property, null=True, on_delete=models.CASCADE)
    year = models.IntegerField()
    taxes = models.IntegerField()
    land = models.IntegerField()
    additions = models.IntegerField()
    total = models.IntegerField()

class School(models.Model):
    name = models.CharField(max_length=50)
    rating = models.IntegerField()
    school_type = models.CharField(max_length=10)
    students = models.IntegerField()
    no_of_reviews = models.IntegerField()
    distance = models.DecimalField(decimal_places=1, max_digits=4, help_text='in miles')
    grades = models.CharField(max_length=10)
    category = models.CharField(max_length=20)


class Agent(models.Model):
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
    def image_location(self, filename):
        format = filename.split('.')[1]
        filename = generate_filename() + '.' + format
        return '/'.join(['property/', self.property.country,
                         self.property.state,
                         self.property.county, self.property.s[:20] + str(randnum), filename])
    
    image = models.ImageField()
    property = models.ForeignKey(Property, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_location, max_length=300)
    base64 = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.property.title