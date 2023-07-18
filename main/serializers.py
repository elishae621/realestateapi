from rest_framework import serializers
from main import models


class CustomHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    def build_nested_field(self, field_name, relation_info, nested_depth):
        """
        Create nested fields for forward and reverse relationships.
        """

        class NestedSerializer(serializers.HyperlinkedModelSerializer):
            class Meta:
                model = relation_info.related_model
                depth = nested_depth - 1
                fields = "__all__"

        field_class = NestedSerializer
        field_kwargs = serializers.get_nested_relation_kwargs(relation_info)

        return field_class, field_kwargs


class CustomListField(serializers.ListField):
    def to_representation(self, data):
        """
        List of object instances -> List of dicts of primitive datatypes.
        """
        return [
            self.child.to_representation(item.name) if item is not None else None
            for item in data.all()
        ]

class FlagRelatedField(serializers.RelatedField):
    def to_representation(self, data):
        """
        List of object instances -> List of dicts of primitive datatypes.
        """
        flags = dict(models.Flags.objects.filter(id=data.id).values()[0])
        del flags['id']
        del flags['property_id']
        return flags
    
class ImageTagRelatedField(serializers.RelatedField):
    def to_representation(self, data):
        """
        List of object instances -> List of dicts of primitive datatypes.
        """
        return [
            {'label': item.label, 'probability': str(item.probability)} if item is not None else None
            for item in data.all()
        ]

class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PriceHistory
        fields = ['date', 'event', 'price', 'price_sqft', 'source']
        
class TaxHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaxHistory
        fields = ['year', 'tax', 'land', 'building', 'total']


class SchoolSerializer(serializers.ModelSerializer):
    education_levels = CustomListField()
    grads = CustomListField()
    
    class Meta:
        model = models.School
        fields = ['name', 'latitude', 'longitude', 'education_levels', 'distance_in_miles', 'district', 'greatschools_id', 'nces_code', 'rating', 'grades', 'funding_type', 'student_count', 'review_count', 'parent_rating']

class ImageTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImageTag
        fields = ['label', 'probability']  
        
class PhotosSerializer(serializers.ModelSerializer):
    tags = ImageTagRelatedField(read_only=True)
    class Meta:
        model = models.Image
        fields = ['image', 'tags']
         

class PropertySerializer(CustomHyperlinkedModelSerializer):
    other_property_info = CustomListField()
    tags = CustomListField()
    waterfront_water_access = CustomListField()
    land_info = CustomListField()
    school_information = CustomListField()
    hoa = CustomListField()
    utilities = CustomListField()
    location = serializers.SerializerMethodField("get_location")
    features = serializers.SerializerMethodField("get_features")
    environmental_risk = serializers.SerializerMethodField("get_environmental_risk")
    url = serializers.HyperlinkedIdentityField(
        view_name="property-detail", lookup_field="slug"
    )
    agent = serializers.HyperlinkedRelatedField(
        view_name="agent-detail", lookup_field="agent_id", read_only=True
    )
    neighborhood = serializers.RelatedField(read_only=True)
    flags = FlagRelatedField(read_only=True)
    price_history = PriceHistorySerializer(many=True)
    tax_history = TaxHistorySerializer(many=True)
    nearby_schools = SchoolSerializer(many=True)
    photos = PhotosSerializer(many=True)

    def get_environmental_risk(self, obj):
        return {
            "wildfire": {
                "fire_factor_severity": obj.fire_factor_severity,
                "fire_trend": obj.fire_trend,
            },
            "flood": {
                "flood_factor_severity": obj.flood_factor_severity,
                "flood_trend": obj.flood_trend,
            },
            "noice_score": obj.noice_score,
        }

    def get_location(self, obj):
        return {
            "address": obj.address,
            "latitude": obj.latitude,
            "longitude": obj.longitude,
            "unit": obj.unit,
            "city": obj.city,
            "state_code": obj.state_code,
            "state": obj.state,
            "postal_code": obj.postal_code,
            "county": obj.county,
            "country": obj.country,
            "street_view_url": obj.street_view_url,
            "street_view_metadata_url": obj.street_view_url,
            "street_number": obj.street_number,
            "street_direction": obj.street_direction,
            "street_name": obj.street_name,
            "street_suffix": obj.street_suffix,
            "street_post_direction": obj.street_post_direction,
            "driving_directions": obj.driving_directions,
        }

    def get_features(self, obj):
        return {
            "baths": obj.baths,
            "baths_consolidated": obj.baths_consolidated,
            "baths_full": obj.baths_full,
            "baths_3qtr": obj.baths_3qtr,
            "baths_half": obj.baths_half,
            "baths_total": obj.baths_total,
            "beds": obj.beds,
            "garage": obj.garage,
            "garage_type": obj.garage_type,
            "construction": obj.construction,
            "cooling": obj.cooling,
            "exterior": obj.exterior,
            "fireplace": obj.fireplace,
            "heating": obj.heating,
            "roofing": obj.roofing,
            "pool": obj.pool,
            "units": obj.units,
            "unit_count": obj.unit_count,
            "stories": obj.stories,
            "sqft": obj.sqft,
            "lot_sqft": obj.lot_sqft,
            "rooms": obj.rooms,
        }

    class Meta:
        model = models.Property
        fields = [
            "url",
            "slug",
            "status",
            "type",
            "sub_type",
            "location",
            "features",
            "primary_photo",
            "agent",
            "text",
            "environmental_risk",
            "coming_soon_date",
            "list_price",
            "last_price_change_amount",
            "last_sold_price",
            "price_per_sqft",
            "list_date",
            "waterfront_water_access",
            "land_info",
            "school_information",
            "hoa",
            "utilities",
            "builder",
            "other_property_info",
            "year_built",
            "year_renovated",
            "name",
            "zoning",
            "neighborhood",
            "tags",
            "flags",
            "price_history",
            "tax_history",
            "nearby_schools",
            "photos_count",
            "photos",
        ]


class AgentSerializer(CustomHyperlinkedModelSerializer):
    class Meta:
        model = models.Agent
        fields = "__all__"


class SchoolSerializer(CustomHyperlinkedModelSerializer):
    class Meta:
        model = models.Property
        fields = "__all__"


class NeighborhoodSerializer(CustomHyperlinkedModelSerializer):
    class Meta:
        model = models.Property
        fields = "__all__"
