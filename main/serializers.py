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
                fields = '__all__'

        field_class = NestedSerializer
        field_kwargs = serializers.get_nested_relation_kwargs(relation_info)

        return field_class, field_kwargs

class CustomListField(serializers.ListField):
    def to_representation(self, data):
        """
        List of object instances -> List of dicts of primitive datatypes.
        """
        return [self.child.to_representation(item.name) if item is not None else None for item in data.all()]


class PropertySerializer(CustomHyperlinkedModelSerializer):
    other_property_info = CustomListField()
    tags = CustomListField()
    waterfront_water_access = CustomListField()
    land_info = CustomListField()
    school_information = CustomListField()
    hoa = CustomListField()
    utilities = CustomListField()
    
    class Meta:
        model = models.Property
        # fields = ['url', 'address', 'slug', 'agent', 'primary_photo', 'flood_factor_severity', 'flood_trend','fire_factor_severity', 'other_property_info']
        exclude = ['source_url']

class AgentSerializer(CustomHyperlinkedModelSerializer):
    class Meta:
        model = models.Agent
        fields = '__all__'

class SchoolSerializer(CustomHyperlinkedModelSerializer):
    class Meta:
        model = models.Property
        fields = '__all__'

class NeighborhoodSerializer(CustomHyperlinkedModelSerializer):
    class Meta:
        model = models.Property
        fields = '__all__'
        
class ListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ListItem
        fields = '__all__'
