# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from main import models
from dateutil.parser import parse
from decimal import Decimal
import json
import logging

def extract(item, filters, date=False, image=False, decimal=False, list=False):
    filters_list = filters.split(",")
    try:
        while filters_list and item:
            item = item[filters_list[0]]
            filters_list.pop(0)
    except KeyError:
        return None if not list else []
    if item and image:
        item.replace('.jpg', '-w480_h360_x2.jpg')
    if item and decimal:
        item = Decimal(item)
    if item and date:
        item = parse(item)
    if item == None and list:
        return []
    return item

class PropertyPipeline:
    def process_item(self, item, spider):
        propertyDetails = extract(item, 'property')
        if not propertyDetails:
            return item
        logging.info("saving property")
        property, created = models.Property.objects.get_or_create(
            address=extract(propertyDetails, 'location,address,line'),
            source_url=extract(propertyDetails, 'href'))
        property.flood_factor_severity=extract(propertyDetails, 'local,flood,flood_factor_severity')
        property.flood_factor_severity=extract(propertyDetails, 'local,flood,flood_factor_severity')
        property.flood_trend=extract(propertyDetails, 'local,flood,flood_trend')
        property.fire_factor_severity=extract(propertyDetails, 'local,wildfire,fire_factor_severity')
        property.fire_trend=extract(propertyDetails, 'local,wildfire,fire_trend')
        property.status=extract(propertyDetails, 'status')
        property.coming_soon_date=extract(propertyDetails, 'coming_soon_date', date=True)
        property.list_price=extract(propertyDetails, 'list_price')
        property.last_price_change_amount=extract(propertyDetails, 'last_price_change_amount')
        property.last_sold_date=extract(propertyDetails, 'last_sold_date', date=True)
        property.last_sold_price=extract(propertyDetails, 'last_sold_price')
        property.price_per_sqft=extract(propertyDetails, 'price_per_sqft')
        property.list_date=extract(propertyDetails, 'list_date', date=True)
        property.street_view_url=extract(propertyDetails, 'location,address,street_view_url')
        property.street_view_metadata_url=extract(propertyDetails, 'location,address,street_view_metadata_url')
        property.street_number=extract(propertyDetails, 'location,address,street_number')
        property.street_direction=extract(propertyDetails, 'location,address,street_direction')
        property.street_name=extract(propertyDetails, 'location,address,street_name')
        property.street_suffix=extract(propertyDetails, 'location,address,street_suffix')
        property.street_post_direction=extract(propertyDetails, 'location,address,street_post_direction')
        property.unit=extract(propertyDetails, 'location,address,unit')
        property.county=extract(propertyDetails, 'location,county,name')
        property.city=extract(propertyDetails, 'location,address,city')
        property.state_code=extract(propertyDetails, 'location,address,state_code')
        property.postal_code=extract(propertyDetails, 'location,address,postal_code')
        property.country=extract(propertyDetails, 'location,address,country')
        property.validation_code=extract(propertyDetails, 'location,address,validation_code')
        property.state=extract(propertyDetails, 'location,address,state')
        property.latitude=extract(propertyDetails, 'location,address,coordinate,lat', decimal=True)
        property.longitude=extract(propertyDetails, 'location,address,coordinate,lon', decimal=True)
        property.driving_directions=extract(propertyDetails, 'location,driving_directions')
        property.builder=extract(propertyDetails, 'builder')
        property.baths=extract(propertyDetails, 'description,baths')
        property.baths_consolidated=extract(propertyDetails, 'description,baths_consolidated')
        property.baths_full=extract(propertyDetails, 'description,baths_full')
        property.baths_3qtr=extract(propertyDetails, 'description,baths_3qtr')
        property.baths_half=extract(propertyDetails, 'description,baths_half')
        property.baths_total=extract(propertyDetails, 'description,baths_total')
        property.beds=extract(propertyDetails, 'description,beds')
        property.construction=extract(propertyDetails, 'description,construction')
        property.cooling=extract(propertyDetails, 'description,cooling')
        property.exterior=extract(propertyDetails, 'description,exterior')
        property.fireplace=extract(propertyDetails, 'description,fireplace')
        property.garage=extract(propertyDetails, 'description,garage')
        property.garage_type=extract(propertyDetails, 'description,garage_type')
        property.heating=extract(propertyDetails, 'description,heating')
        property.roofing=extract(propertyDetails, 'description,roofing')
        property.pool=extract(propertyDetails, 'description,pool')
        property.sqft=extract(propertyDetails, 'description,sqft')
        property.lot_sqft=extract(propertyDetails, 'description,lot_sqft')
        property.rooms=extract(propertyDetails, 'description,rooms')
        property.stories=extract(propertyDetails, 'description,stories')
        property.sub_type=extract(propertyDetails, 'description,sub_type')
        property.text=extract(propertyDetails, 'description,text')
        property.type=extract(propertyDetails, 'description,type')
        property.units=extract(propertyDetails, 'description,units')
        property.year_built=extract(propertyDetails, 'description,year_built')
        property.year_renovated=extract(propertyDetails, 'description,year_renovated')
        property.zoning=extract(propertyDetails, 'description,zoning')
        property.name=extract(propertyDetails, 'description,name')
        property.primary_photo=extract(propertyDetails, 'primary_photo,href', image=True)
        property.save()
            
        models.Image.objects.filter(property=property).delete()
        for photo in extract(propertyDetails, 'photos', list=True):
            image = models.Image.objects.create(
                property=property,
                image=extract(photo, 'href').replace('.jpg', '-w480_h360_x2.jpg')
            )
            models.ImageTag.objects.filter(image=image).delete()
            for tag in extract(photo, 'tags', list=True):
                models.ImageTag.objects.create(
                    image=image,
                    label=extract(tag, 'label'),
                    probability=extract(tag, 'probability')
                )
                
        for detail in extract(propertyDetails, 'details', list=True):
            if extract(detail, 'category') == "Waterfront and Water Access": 
                for element in extract(detail, 'text', list=True):
                    if not property.waterfront_water_access.filter(name=element):
                        property.waterfront_water_access.add(models.ListItem.objects.create(name=element))
                        property.save()
            if extract(detail, 'category') == "Land Info": 
                for element in extract(detail, 'text', list=True):
                    if not property.land_info.filter(name=element):
                        property.land_info.add(models.ListItem.objects.create(name=element))
                        property.save()
            if extract(detail, 'category') == "School Information": 
                for element in extract(detail, 'text', list=True):
                    if not property.school_information.filter(name=element):
                        property.school_information.add(models.ListItem.objects.create(name=element))
                        property.save()
            if extract(detail, 'category') == "Homeowners Association": 
                for element in extract(detail, 'text', list=True):
                    if not property.hoa.filter(name=element):
                        property.hoa.add(models.ListItem.objects.create(name=element))
                        property.save()
            if extract(detail, 'category') == "Other Property Info": 
                for element in extract(detail, 'text', list=True):
                    if not property.other_property_info.filter(name=element):
                        property.other_property_info.add(models.ListItem.objects.create(name=element))
                        property.save()
            if extract(detail, 'category') == "Utilities": 
                for element in extract(detail, 'text', list=True):
                    if not property.utilities.filter(name=element):
                        property.utilities.add(models.ListItem.objects.create(name=element))
                        property.save()
                        
        property.pricehistory_set.all().delete()
        for history in extract(propertyDetails, 'property_history', list=True):
            models.PriceHistory.objects.create(
                date=extract(history, 'date', date=True),
                event=extract(history, 'event_name'),
                price=extract(history, 'price'),
                source=extract(history, 'source_name'),
                price_sqft=extract(history, 'price_sqft'),
                property=property
            )
            
        property.taxhistory_set.all().delete()
        for tax in extract(propertyDetails, 'tax_history', list=True):
            models.TaxHistory.objects.create(
                year=extract(tax, 'year'),
                tax=extract(tax, 'tax'),
                land=extract(tax, 'assessment,land'),
                building=extract(tax, 'assessment,building'),
                total=extract(tax, 'assessment,total'),
                property=property
            )
            
        if extract(propertyDetails, 'neighborhood'):
            neighborhood, created = models.Neighborhood.objects.get_or_create(local_url=extract(propertyDetails, 'neighborhood,local_url'))
            models.Neighborhood.objects.filter(local_url=neighborhood.local_url).update(
                area=extract(propertyDetails, 'neighborhood,area'),
                median_price_per_sqft=extract(propertyDetails, 'neighborhood,median_price_per_sqft'),
                median_listing_price=extract(propertyDetails, 'neighborhood,median_listing_price'),
                median_sold_price=extract(propertyDetails, 'neighborhood,median_sold_price'),
                median_days_on_market=extract(propertyDetails, 'neighborhood,median_days_on_market'),
                hot_market_badge=extract(propertyDetails, 'neighborhood,hot_market_badge'),
            )
        
            for nbh in extract(propertyDetails, 'nearby_neighborhoods', list=True):
                nearby_nbh, created = models.Neighborhood.objects.get_or_create(local_url=extract(nbh, 'local_url'))
                models.Neighborhood.objects.filter(local_url=nearby_nbh.local_url).update(
                    area=extract(nbh, 'area'),
                    median_listing_price=extract(nbh, 'median_listing_price'),
                )
                
                neighborhood.nearby_neighborhoods.add(nearby_nbh)
                neighborhood.save()

            
        for school in extract(propertyDetails, 'school', list=True):
            sch = models.School.objects.get_or_create(
                longitude=extract(school, 'coordinate,lon', decimal=True),
                latitude=extract(school, 'coordinate,lat', decimal=True),
            )
            models.School.objects.filter(id=sch.id).update(
                distance_in_miles=extract(school, 'distance_in_miles'),
                district=extract(school, 'district,name'),
                funding_type=extract(school, 'funding_type'),
                greatschools_id=extract(school, 'greatschools_id'),
                name=extract(school, 'name'),
                nces_code=extract(school, 'nces_code'),
                parent_rating=extract(school, 'parent_rating'),
                review_count=extract(school, 'review_count'),
                student_count=extract(school, 'student_count'),
            )
            sch.education_levels.all().delete()
            for level in extract(school, 'education_levels', list=True):
                sch.education_levels.add(models.ListItem.objects.create(name=level))
                sch.save()
                
            sch.grads.all().delete()
            for grade in extract(school, 'grades', list=True):
                sch.grades.add(models.ListItem.objects.create(name=grade))
                sch.save()
            
            property.schools.add(sch)
            property.save()
            
        property.tags.all().delete()
        for tag in extract(propertyDetails, 'tags', list=True):
            property.tags.add(models.ListItem.objects.create(name=tag))
            property.save()
            
        flag, created = models.Flags.objects.get_or_create(
            property=property
        )
        models.Flags.objects.filter(id=flag.id).update(
            is_pending=extract(propertyDetails, 'flags,is_pending'),
            is_contingent=extract(propertyDetails, 'flags,is_contingent'),
            is_new_listing=extract(propertyDetails, 'flags,is_new_listing'),
            is_new_construction=extract(propertyDetails, 'flags,is_new_construction'),
            is_short_sale=extract(propertyDetails, 'flags,is_short_sale'),
            is_foreclosure=extract(propertyDetails, 'flags,is_foreclosure'),
            is_price_reduced=extract(propertyDetails, 'flags,is_price_reduced'),
            is_senior_community=extract(propertyDetails, 'flags,is_senior_community'),
            is_deal_available=extract(propertyDetails, 'flags,is_deal_available'),
            is_for_rent=extract(propertyDetails, 'flags,is_for_rent'),
            is_garage_present=extract(propertyDetails, 'flags,is_garage_present'),
            is_price_excludes_land=extract(propertyDetails, 'flags,is_price_excludes_land'),
            is_subdivision=extract(propertyDetails, 'flags,is_subdivision'),
            is_coming_soon=extract(propertyDetails, 'flags,is_coming_soon'),    
        )
        for advertiser in extract(propertyDetails, 'consumer_advertisers', list=True):
            if extract(advertiser, 'type') == 'Agent':
                agent, created = models.Agent.objects.get_or_create(
                    agent_id=extract(advertiser, 'agent_id'),
                )
                property.agent = agent
                property.save()
                
        return item

class AgentPipeline:
    def process_item(self, item, spider):
        agentDetails = extract(item, 'agent')
        if not agentDetails:
            return item
        logging.info("saving agent")
            
        agent, created = models.Agent.objects.get_or_create(agent_id=extract(agentDetails, 'advertiser_id'))
        agent.broker_address=extract(agentDetails, 'office,address,line')
        agent.city=extract(agentDetails, 'office,address,city')
        agent.postal_code=extract(agentDetails, 'office,address,postal_code')
        agent.state_code=extract(agentDetails, 'office,address,state_code')
        agent.country=extract(agentDetails, 'office,address,country')
        agent.broker=extract(agentDetails, 'broker,name')
        agent.description=extract(agentDetails, 'description')
        agent.website=extract(agentDetails, 'href')
        agent.last_updated=extract(agentDetails, 'last_updated', date=True)
        agent.save()
        
        for area in extract(agentDetails, 'served_areas', list=True):
            models.ServedAreas.objects.get_or_create(
                name=extract(area, 'name'),
                state_code=extract(area, 'state_code'),
                agent=agent,
            )
        
        agent.specializations.all().delete()
        for specialization in extract(agentDetails, 'specializations', list=True):
            agent.specializations.add(models.ListItem.objects.create(name=extract(specialization, 'name')))
            agent.save()
            
        agent.zips.all().delete()
        for zip in extract(agentDetails, 'zips', list=True):
            agent.zips.add(models.ListItem.objects.create(name=zip))
            agent.save()

        agent.phones.all().delete()
        for phone in extract(agentDetails, 'phones', list=True):
            agent.phones.add(models.ListItem.objects.create(name=extract(phone, 'number')))
            agent.save()
        
        return item 