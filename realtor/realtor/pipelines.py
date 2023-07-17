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

def extract(item, filters, date=False, image=False, decimal=False):
    filters_list = filters.split(",")
    value = item
    try:
        while filters_list and value:
            value = value[filters_list[0]]
            filters_list.pop(0)
    except KeyError:
        return None
    if value and image:
        value.replace('.jpg', '-w480_h360_x2.jpg')
    if value and decimal:
        value = Decimal(value)
    if value and date:
        value = parse(value)
    return value

class PropertyPipeline:
    def process_item(self, item, spider):
        propertyDetails = extract(item, 'property')
        if not propertyDetails:
            return item
        logging.info("saving property")
        property, created = models.Property.objects.get_or_create(
            source_url=extract(propertyDetails, 'href'))
        models.Property.objects.filter(id=property.id).update(
            flood_factor_severity=extract(propertyDetails, 'local,flood,flood_factor_severity'),
            flood_trend=extract(propertyDetails, 'local,flood,flood_trend'),
            fire_factor_severity=extract(propertyDetails, 'local,wildfire,fire_factor_severity'),
            fire_trend=extract(propertyDetails, 'local,wildfire,fire_trend'),
            status=extract(propertyDetails, 'status'),
            coming_soon_date=extract(propertyDetails, 'coming_soon_date', date=True),
            list_price=extract(propertyDetails, 'list_price'),
            last_price_change_amount=extract(propertyDetails, 'last_price_change_amount'),
            last_sold_date=extract(propertyDetails, 'last_sold_date', date=True),
            last_sold_price=extract(propertyDetails, 'last_sold_price'),
            price_per_sqft=extract(propertyDetails, 'price_per_sqft'),
            list_date=extract(propertyDetails, 'list_date', date=True),
            address=extract(propertyDetails, 'location,address,line'),
            street_view_url=extract(propertyDetails, 'location,address,street_view_url'),
            street_view_metadata_url=extract(propertyDetails, 'location,address,street_view_metadata_url'),
            street_number=extract(propertyDetails, 'location,address,street_number'),
            street_direction=extract(propertyDetails, 'location,address,street_direction'),
            street_name=extract(propertyDetails, 'location,address,street_name'),
            street_suffix=extract(propertyDetails, 'location,address,street_suffix'),
            street_post_direction=extract(propertyDetails, 'location,address,street_post_direction'),
            unit=extract(propertyDetails, 'location,address,unit'),
            county=extract(propertyDetails, 'location,county,name'),
            city=extract(propertyDetails, 'location,address,city'),
            state_code=extract(propertyDetails, 'location,address,state_code'),
            postal_code=extract(propertyDetails, 'location,address,postal_code'),
            country=extract(propertyDetails, 'location,address,country'),
            validation_code=extract(propertyDetails, 'location,address,validation_code'),
            state=extract(propertyDetails, 'location,address,state'),
            latitude=extract(propertyDetails, 'location,address,coordinate,lat', decimal=True),
            longitude=extract(propertyDetails, 'location,address,coordinate,lon', decimal=True),
            driving_directions=extract(propertyDetails, 'location,driving_directions'),
            builder=extract(propertyDetails, 'builder'),
            baths=extract(propertyDetails, 'description,baths'),
            baths_consolidated=extract(propertyDetails, 'description,baths_consolidated'),
            baths_full=extract(propertyDetails, 'description,baths_full'),
            baths_3qtr=extract(propertyDetails, 'description,baths_3qtr'),
            baths_half=extract(propertyDetails, 'description,baths_half'),
            baths_total=extract(propertyDetails, 'description,baths_total'),
            beds=extract(propertyDetails, 'description,beds'),
            construction=extract(propertyDetails, 'description,construction'),
            cooling=extract(propertyDetails, 'description,cooling'),
            exterior=extract(propertyDetails, 'description,exterior'),
            fireplace=extract(propertyDetails, 'description,fireplace'),
            garage=extract(propertyDetails, 'description,garage'),
            garage_type=extract(propertyDetails, 'description,garage_type'),
            heating=extract(propertyDetails, 'description,heating'),
            roofing=extract(propertyDetails, 'description,roofing'),
            pool=extract(propertyDetails, 'description,pool'),
            sqft=extract(propertyDetails, 'description,sqft'),
            lot_sqft=extract(propertyDetails, 'description,lot_sqft'),
            rooms=extract(propertyDetails, 'description,rooms'),
            stories=extract(propertyDetails, 'description,stories'),
            sub_type=extract(propertyDetails, 'description,sub_type'),
            text=extract(propertyDetails, 'description,text'),
            type=extract(propertyDetails, 'description,type'),
            units=extract(propertyDetails, 'description,units'),
            year_built=extract(propertyDetails, 'description,year_built'),
            year_renovated=extract(propertyDetails, 'description,year_renovated'),
            zoning=extract(propertyDetails, 'description,zoning'),
            name=extract(propertyDetails, 'description,name'),
            primary_photo=extract(propertyDetails, 'primary_photo,href', image=True)
        )
            
        models.Image.objects.filter(property=property).delete()
        for photo in extract(propertyDetails, 'photos'):
            image = models.Image.objects.create(
                property=property,
                image=extract(photo, 'href').replace('.jpg', '-w480_h360_x2.jpg')
            )
            models.ImageTag.objects.filter(image=image).delete()
            for tag in extract(photo, 'tags'):
                models.ImageTag.objects.create(
                    image=image,
                    label=extract(tag, 'label'),
                    probability=extract(tag, 'probability')
                )
                
        for detail in extract(propertyDetails, 'details'):
            if extract(detail, 'category') == "Waterfront and Water Access": 
                for element in extract(detail, 'text'):
                    if not property.waterfront_water_access.filter(name=element):
                        property.waterfront_water_access.add(models.ListItem.objects.create(name=element))
                        property.save()
            if extract(detail, 'category') == "Land Info": 
                for element in extract(detail, 'text'):
                    if not property.land_info.filter(name=element):
                        property.land_info.add(models.ListItem.objects.create(name=element))
                        property.save()
            if extract(detail, 'category') == "School Information": 
                for element in extract(detail, 'text'):
                    if not property.school_information.filter(name=element):
                        property.school_information.add(models.ListItem.objects.create(name=element))
                        property.save()
            if extract(detail, 'category') == "Homeowners Association": 
                for element in extract(detail, 'text'):
                    if not property.hoa.filter(name=element):
                        property.hoa.add(models.ListItem.objects.create(name=element))
                        property.save()
            if extract(detail, 'category') == "Other Property Info": 
                for element in extract(detail, 'text'):
                    if not property.other_property_info.filter(name=element):
                        property.other_property_info.add(models.ListItem.objects.create(name=element))
                        property.save()
            if extract(detail, 'category') == "Utilities": 
                for element in extract(detail, 'text'):
                    if not property.utilities.filter(name=element):
                        property.utilities.add(models.ListItem.objects.create(name=element))
                        property.save()
                        
        for history in extract(propertyDetails, 'property_history'):
            property.pricehistory_set.all().delete()
            models.PriceHistory.objects.create(
                date=extract(history, 'date', date=True),
                event=extract(history, 'event_name'),
                price=extract(history, 'price'),
                source=extract(history, 'source_name'),
                price_sqft=extract(history, 'price_sqft'),
                property=property
            )
            
        for tax in extract(propertyDetails, 'tax_history'):
            property.taxhistory_set.all().delete()
            models.TaxHistory.objects.create(
                year=extract(tax, 'year'),
                taxes=extract(tax, 'taxes'),
                land=extract(tax, 'land'),
                additions=extract(tax, 'additions'),
                total=extract(tax, 'total'),
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
        
            for nbh in extract(propertyDetails, 'nearby_neighborhoods'):
                nearby_nbh, created = models.Neighborhood.objects.get_or_create(local_url=extract(nbh, 'local_url'))
                models.Neighborhood.objects.filter(local_url=nearby_nbh.local_url).update(
                    area=extract(nbh, 'area'),
                    median_listing_price=extract(nbh, 'median_listing_price'),
                )
                
                neighborhood.nearby_neighborhoods.add(nearby_nbh)
                neighborhood.save()

            
        for school in extract(propertyDetails, 'school'):
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
            for level in extract(school, 'education_levels'):
                sch.education_levels.all().delete()
                sch.education_levels.add(models.ListItem.objects.create(name=level))
                sch.save()
                
            for grade in extract(school, 'grades'):
                sch.grads.all().delete()
                sch.grades.add(models.ListItem.objects.create(name=grade))
                sch.save()
            
            property.schools.add(sch)
            property.save()
            
        for tag in extract(propertyDetails, 'tags'):
            property.tags.all().delete()
            property.tags.add(models.ListItem.objects.create(name=extract(tag)))
            property.save()
            
        flag = models.Flags.objects.get_or_create(
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
        for advertiser in extract(propertyDetails, 'consumer_advertisers'):
            if extract(advertiser, 'type') == 'Agent':
                agent, created = models.Agent.objects.get_or_create(
                    agent_id=extract(advertiser, 'agent_id'),
                )
                property.agent = agent
                property.save()
                
        return propertyDetails

class AgentPipeline:
    def process_item(self, item, spider):
        agentDetails = extract(item, 'agent')
        if not agentDetails:
            return item
        logging.info("saving agent")
        agent, created = models.Agent.objects.get_or_create(agent_id=extract(agentDetails, 'advertiser_id'))
        models.Agent.objects.filter(id=agent.id).update(
            broker_address=extract(agentDetails, 'office,address,line'),
            city=extract(agentDetails, 'office,address,city'),
            postal_code=extract(agentDetails, 'office,address,postal_code'),
            state_code=extract(agentDetails, 'office,address,state_code'),
            country=extract(agentDetails, 'office,address,country'),
            broker=extract(agentDetails, 'broker,name'),
            description=extract(agentDetails, 'description'),
            website=extract(agentDetails, 'href'),
            name=extract(agentDetails, 'name'),
            last_updated=extract(agentDetails, 'last_updated', date=True),
        )
        
        for area in extract(agentDetails, 'served_areas'):
            models.ServedAreas.objects.get_or_create(
                name=extract(area, 'name'),
                state_code=extract(area, 'state_code'),
                agent=agent,
            )
            
        for specialization in extract(agentDetails, 'specializations'):
            agent.specializations.all().delete()
            agent.specializations.add(models.ListagentDetails.objects.create(name=extract(specialization, 'name')))
            agent.save()
            
        for zip in extract(agentDetails, 'zips'):
            agent.zips.all().delete()
            agent.zips.add(models.ListagentDetails.objects.create(name=zip))
            agent.save()

        for phone in extract(agentDetails, 'phones'):
            agent.phones.all().delete()
            agent.phones.add(models.ListagentDetails.objects.create(name=extract(phone, 'number')))
            agent.save()
        
        return agent 