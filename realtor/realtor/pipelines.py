# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from main.models import Property, Image, ImageTag, PriceHistory, Agent, Flags, ListItem, TaxHistory
from dateutil.parser import parse
from decimal import Decimal

def extract(value):
    return value if value else None

class RealtorPipeline:
    def process_item(self, item, spider):
        self.logger.info("saving property")
        property = Property.objects.create(
            flood_factor_score=extract(item['local']['flood']['flood_factor_score']),
            flood_fema_zone=extract(item['local']['flood']['femazone'][0]),
            move_in_date=extract(item['move_in_date']),
            status=extract(item['for_sale']),
            coming_soon_date=extract(item['coming_soon_date']),
            source_url=extract(item['href']),
            list_price=extract(item['list_price']),
            last_price_change_amount=extract(item['last_price_change_amount']),
            list_price_min=extract(item['list_price_min']),
            list_price_max=extract(item['list_price_max']),
            price_per_sqft=extract(item['price_per_sqft']),
            list_date=extract(item['list_date']),
            address=extract(item['location']['address']),
            street_number=extract(item['location']['street_number']),
            street_direction=extract(item['location']['street_direction']),
            street_name=extract(item['location']['street_name']),
            street_suffix=extract(item['location']['street_suffix']),
            street_post_direction=extract(item['location']['street_post_direction']),
            unit=extract(item['location']['unit']),
            city=extract(item['location']['city']),
            state_code=extract(item['location']['state_code']),
            postal_code=extract(item['location']['postal_code']),
            country=extract(item['location']['country']),
            validation_code=extract(item['location']['validation_code']),
            state=extract(item['location']['state']),
            latitude=Decimal(extract(item['location']['lat'])),
            longitude=Decimal(extract(item['location']['lon'])),
            cross_street=extract(item['location']['cross_street']),
            driving_directions=extract(item['location']['driving_directions']),
            builder=extract(item['builder']),
            baths=extract(item['description']['baths']),
            baths_consolidated=extract(item['description']['baths_consolidated']),
            baths_full=extract(item['description']['baths_full']),
            baths_3qtr=extract(item['description']['baths_3qtr']),
            baths_half=extract(item['description']['baths_half']),
            baths_1qtr=extract(item['description']['baths_1qtr']),
            baths_min=extract(item['description']['baths_min']),
            baths_max=extract(item['description']['baths_max']),
            beds_min=extract(item['description']['beds_min']),
            beds_max=extract(item['description']['beds_max']),
            beds=extract(item['description']['beds']),
            pool=extract(item['description']['pool']),
            sqft=extract(item['description']['sqft']),
            sqft_min=extract(item['description']['sqft_min']),
            sqft_max=extract(item['description']['sqft_max']),
            lot_sqft=extract(item['description']['lot_sqft']),
            rooms=extract(item['description']['rooms']),
            stories=extract(item['description']['stories']),
            sub_type=extract(item['description']['sub_type']),
            text=extract(item['description']['text']),
            type=extract(item['description']['type']),
            units=extract(item['description']['units']),
            unit_type=extract(item['description']['unit_type']),
            year_built=extract(item['description']['year_built']),
            name=extract(item['description']['name']),
        )
        for photo in item['photos']:
            image = Image.objects.create(
                property=property,
                image=photo['href'].replace('.jpg', '-w480_h360_x2.jpg')
            )
            for tag in photo['tags']:
                ImageTag.objects.create(
                    image=image,
                    label=tag['label'],
                    probability=tag['probability']
                )
            
        for detail in item['details']:
            if detail['category'] == "Waterfront and Water Access": 
                for item in item['details']['text']:
                    property.waterfront_water_access.add(ListItem.objects.create(name=extract(item)))
                    property.save()
            if detail['category'] == "Land Info": 
                for item in item['details']['text']:
                    property.land_info.add(ListItem.objects.create(name=extract(item)))
                    property.save()
            if detail['category'] == "School Information": 
                for item in item['details']['text']:
                    property.school_information.add(ListItem.objects.create(name=extract(item)))
                    property.save()
            if detail['category'] == "Homeowners Association": 
                for item in item['details']['text']:
                    property.hoa.add(ListItem.objects.create(name=extract(item)))
                    property.save()
            if detail['category'] == "Other Property Info": 
                for item in item['details']['text']:
                    property.other_property_info.add(ListItem.objects.create(name=extract(item)))
                    property.save()
            if detail['category'] == "Utilities": 
                for item in item['details']['text']:
                    property.utilities.add(ListItem.objects.create(name=extract(item)))
                    property.save()
        for history in item['property_history']:
            PriceHistory.objects.create(
                date=parse(history['date']),
                event=extract(history['event_name']),
                price=extract(history['price']),
                source=extract(history['source_name']),
                price_sqft=extract(history['price_sqft']),
                property=property
            )
        for tax in item['tax_history']:
            TaxHistory.objects.create(
                year=parse(tax['year']),
                taxes=extract(tax['taxes']),
                land=extract(tax['land']),
                additions=extract(tax['additions']),
                total=extract(tax['total']),
                property=property
            )
        for tag in item['tags']:
            property.tags.add(ListItem.objects.create(name=extract(tag)))
            property.save()
        Flags.objects.create(
            property=property,
            is_pending=extract(item['is_pending']),
            is_contingent=extract(item['is_contingent']),
            is_new_listing=extract(item['is_new_listing']),
            is_new_construction=extract(item['is_new_construction']),
            is_short_sale=extract(item['is_short_sale']),
            is_foreclosure=extract(item['is_foreclosure']),
            is_price_reduced=extract(item['is_price_reduced']),
            is_senior_community=extract(item['is_senior_community']),
            is_deal_available=extract(item['is_deal_available']),
            is_price_excludes_land=extract(item['is_price_excludes_land']),
            is_subdivision=extract(item['is_subdivision']),
            is_coming_soon=extract(item['is_coming_soon']),    
        )
        return item
