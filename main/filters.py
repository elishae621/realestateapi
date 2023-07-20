from main import models
import django_filters


class PropertyFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(
        field_name="tags__name", lookup_expr=["icontains", "isnull"]
    )
    nearby_schools = django_filters.CharFilter(
        field_name="nearby_schools__name", lookup_expr=["icontains", "isnull"]
    )
    waterfront_water_access = django_filters.CharFilter(
        field_name="waterfront_water_access__name", lookup_expr=["icontains", "isnull"]
    )
    land_info = django_filters.CharFilter(
        field_name="land_info__name", lookup_expr=["icontains", "isnull"]
    )
    school_information = django_filters.CharFilter(
        field_name="school_information__name", lookup_expr=["icontains", "isnull"]
    )
    hoa = django_filters.CharFilter(
        field_name="hoa__name", lookup_expr=["icontains", "isnull"]
    )
    other_property_info = django_filters.CharFilter(
        field_name="other_property_info__name", lookup_expr=["icontains", "isnull"]
    )
    utilities = django_filters.CharFilter(
        field_name="utilities__name", lookup_expr=["icontains", "isnull"]
    )

    class Meta:
        model = models.Property
        fields = {
            "address": ["icontains", "isnull", "iexact", "exact", "contains"],
            "slug": ["icontains", "isnull", "iexact", "exact", "contains"],
            "agent__slug": ["icontains", "isnull", "iexact", "exact", "contains"],
            "agent__broker": ["icontains", "isnull", "iexact", "exact", "contains"],
            "neighborhood__name": [
                "icontains",
                "isnull",
                "iexact",
                "exact",
                "contains",
            ],
            "flood_factor_severity": [
                "icontains",
                "isnull",
                "iexact",
                "exact",
                "contains",
            ],
            "fire_factor_severity": [
                "icontains",
                "isnull",
                "iexact",
                "exact",
                "contains",
            ],
            "status": ["icontains", "isnull", "iexact", "exact", "contains"],
            "city": ["icontains", "isnull", "iexact", "exact", "contains"],
            "state_code": ["icontains", "isnull", "iexact", "exact", "contains"],
            "postal_code": ["icontains", "isnull", "iexact", "exact", "contains"],
            "county": ["icontains", "isnull", "iexact", "exact", "contains"],
            "country": ["icontains", "isnull", "iexact", "exact", "contains"],
            "state": ["icontains", "isnull", "iexact", "exact", "contains"],
            "builder": ["icontains", "isnull", "iexact", "exact", "contains"],
            "driving_directions": [
                "icontains",
                "isnull",
                "iexact",
                "exact",
                "contains",
            ],
            "pool": ["icontains", "isnull", "iexact", "exact", "contains"],
            "roofing": ["icontains", "isnull", "iexact", "exact", "contains"],
            "heating": ["icontains", "isnull", "iexact", "exact", "contains"],
            "fireplace": ["icontains", "isnull", "iexact", "exact", "contains"],
            "exterior": ["icontains", "isnull", "iexact", "exact", "contains"],
            "cooling": ["icontains", "isnull", "iexact", "exact", "contains"],
            "construction": ["icontains", "isnull", "iexact", "exact", "contains"],
            "garage_type": ["icontains", "isnull", "iexact", "exact", "contains"],
            "text": ["icontains", "isnull", "iexact", "exact", "contains"],
            "type": ["icontains", "isnull", "iexact", "exact", "contains"],
            "name": ["icontains", "isnull", "iexact", "exact", "contains"],
            "zoning": ["icontains", "isnull", "iexact", "exact", "contains"],
            "list_price": ["exact", "lt", "gt", "isnull"],
            "list_price_min": ["exact", "lt", "gt", "isnull"],
            "list_price_max": ["exact", "lt", "gt", "isnull"],
            "noice_score": ["exact", "lt", "gt", "isnull"],
            "coming_soon_date": ["exact", "lt", "gt", "isnull"],
            "last_price_change_amount": ["exact", "lt", "gt", "isnull"],
            "price_per_sqft": ["exact", "lt", "gt", "isnull"],
            "list_date": ["exact", "lt", "gt", "isnull"],
            "latitude": ["exact", "lt", "gt", "isnull"],
            "longitude": ["exact", "lt", "gt", "isnull"],
            "baths": ["exact", "lt", "gt", "isnull"],
            "baths_min": ["exact", "lt", "gt", "isnull"],
            "baths_max": ["exact", "lt", "gt", "isnull"],
            "baths_consolidated": ["exact", "lt", "gt", "isnull"],
            "beds": ["exact", "lt", "gt", "isnull"],
            "beds_min": ["exact", "lt", "gt", "isnull"],
            "beds_max": ["exact", "lt", "gt", "isnull"],
            "garage": ["exact", "lt", "gt", "isnull"],
            "garage_min": ["exact", "lt", "gt", "isnull"],
            "garage_max": ["exact", "lt", "gt", "isnull"],
            "sqft": ["exact", "lt", "gt", "isnull"],
            "sqft_min": ["exact", "lt", "gt", "isnull"],
            "sqft_max": ["exact", "lt", "gt", "isnull"],
            "lot_sqft": ["exact", "lt", "gt", "isnull"],
            "rooms": ["exact", "lt", "gt", "isnull"],
            "stories": ["exact", "lt", "gt", "isnull"],
            "units": ["exact", "lt", "gt", "isnull"],
            "year_built": ["exact", "lt", "gt", "isnull"],
            "year_renovated": ["exact", "lt", "gt", "isnull"],
            "flags__is_pending": ["exact", "isnull"],
            "flags__is_contingent": ["exact", "isnull"],
            "flags__is_new_listing": ["exact", "isnull"],
            "flags__is_new_construction": ["exact", "isnull"],
            "flags__is_short_sale": ["exact", "isnull"],
            "flags__is_foreclosure": ["exact", "isnull"],
            "flags__is_price_reduced": ["exact", "isnull"],
            "flags__is_senior_community": ["exact", "isnull"],
            "flags__is_deal_available": ["exact", "isnull"],
            "flags__is_price_excludes_land": ["exact", "isnull"],
            "flags__is_subdivision": ["exact", "isnull"],
            "flags__is_coming_soon": ["exact", "isnull"],
            "flags__is_for_rent": ["exact", "isnull"],
            "flags__is_garage_present": ["exact", "isnull"],
        }


class AgentFilter(django_filters.FilterSet):
    specialiations = django_filters.CharFilter(
        field_name="specialiations__name", lookup_expr=["icontains", "isnull"]
    )
    phones = django_filters.CharFilter(
        field_name="phones__name", lookup_expr=["icontains", "isnull"]
    )
    zips = django_filters.CharFilter(
        field_name="zips__name", lookup_expr=["icontains", "isnull"]
    )
    
    class Meta:
        model = models.Agent
        fields = {
            "slug": ["icontains", "isnull", "iexact", "exact", "contains"],
            "city": ["icontains", "isnull", "iexact", "exact", "contains"],
            "postal_code": ["icontains", "isnull", "iexact", "exact", "contains"],
            "state_code": ["icontains", "isnull", "iexact", "exact", "contains"],
            "country": ["icontains", "isnull", "iexact", "exact", "contains"],
            "name": ["icontains", "isnull", "iexact", "exact", "contains"],
            "website": ["icontains", "isnull", "iexact", "exact", "contains"],
            "description": ["icontains", "isnull", "iexact", "exact", "contains"],
            "broker": ["icontains", "isnull", "iexact", "exact", "contains"],
            "broker_address": ["icontains", "isnull", "iexact", "exact", "contains"],
            "last_updated": ["exact", "lt", "gt", "isnull"],
        }

class SchoolFilter(django_filters.FilterSet):
    education_levels = django_filters.CharFilter(
        field_name="zips__name", lookup_expr=["icontains", "isnull"]
    )
    grades = django_filters.CharFilter(
        field_name="zips__name", lookup_expr=["icontains", "isnull"]
    )
    served_areas_name = django_filters.CharFilter(
        field_name="servedareas_set__name", lookup_expr=["icontains", "isnull"]
    )
    served_areas_statecode = django_filters.CharFilter(
        field_name="servedareas_set__state_code", lookup_expr=["icontains", "isnull"]
    )
    
    class Meta:
        model = models.School
        fields = {
            "slug": ["icontains", "isnull", "iexact", "exact", "contains"],
            "name": ["icontains", "isnull", "iexact", "exact", "contains"],
            "district": ["icontains", "isnull", "iexact", "exact", "contains"],
            "greatschools_id": ["icontains", "isnull", "iexact", "exact", "contains"],
            "nces_code": ["icontains", "isnull", "iexact", "exact", "contains"],
            "funding_type": ["icontains", "isnull", "iexact", "exact", "contains"],
            "latitude": ["exact", "lt", "gt", "isnull"],
            "longitude": ["exact", "lt", "gt", "isnull"],
            "rating": ["exact", "lt", "gt", "isnull"],
            "student_count": ["exact", "lt", "gt", "isnull"],
            "review_count": ["exact", "lt", "gt", "isnull"],
            "parent_rating": ["exact", "lt", "gt", "isnull"],
        }
        

class NeighborhoodFilter(django_filters.FilterSet):
    nearby_neighborhoods = django_filters.CharFilter(
        field_name="nearby_neighborhoods__name", lookup_expr=["icontains", "isnull"]
    )
    
    class Meta:
        model = models.Neighborhood
        fields = {
            "slug": ["icontains", "isnull", "iexact", "exact", "contains"],
            "slug_id": ["icontains", "isnull", "iexact", "exact", "contains"],
            "name": ["icontains", "isnull", "iexact", "exact", "contains"],
            "state_code": ["icontains", "isnull", "iexact", "exact", "contains"],
            "city": ["icontains", "isnull", "iexact", "exact", "contains"],
            "median_listing_price": ["exact", "lt", "gt", "isnull"],
        }