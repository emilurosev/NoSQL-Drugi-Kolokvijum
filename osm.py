import xml.etree.ElementTree as ET
from pymongo import MongoClient
import json

filename = 'greece-latest.osm'

client = MongoClient(port=27017)
db = client['nosql_kolokvijum']
cities_collection = db['cities']
streets_collection = db['streets']

cities_collection.delete_many({})
streets_collection.delete_many({})

all_streets = []
all_cities = []
cities_list = []
nw_point = {'lat':40.642178, 'lon':22.942729}
se_point = {'lat':40.625734, 'lon':22.977441}

found_streets = []
tag_keys = {}
tags = {}
cities = {}
streets = {}
locations = {}
seen_streets = set()
count = 0
for event, elem in ET.iterparse(filename):
    # print('====================', event, elem.tag)
    # print(count, elem.tag, elem.attrib)
    city = None
    street = None
    for ee in elem:
        # print(ee.tag, ee.attrib)
        for atrelem in ee.attrib:
            # print(atrelem)
            for key in ee.attrib:
                if key == 'k':
                    key_value = ee.attrib[key]
                    if key_value not in tag_keys:
                        tag_keys[key_value] = 0
                    tag_keys[key_value] += 1

            if 'k' in ee.attrib and 'v' in ee.attrib:
                key = ee.attrib['k']
                value = ee.attrib['v']
                if key == 'addr:city':
                    city = value
                if key == 'addr:street':
                    street = value
    if city is not None and street is not None:
        if city not in cities:
            cities[city] = 0
        cities[city] += 1
        addr = city + '\t'+street
        if addr not in streets:
            streets[addr] = 0
            locations[addr.split('\t')[1]] = []
            if elem.attrib.get('lat') is not None and elem.attrib.get('lon') is not None:
                locations[addr.split('\t')[1]].append({'lat': float(elem.attrib.get('lat')), 'lon': float(elem.attrib.get('lon'))})
        streets[addr] += 1
   
    if elem.tag not in tags:
        tags[elem.tag] = 0
    tags[elem.tag] += 1

    if count%100000 == 0:
        stag = [[k, v] for k, v in sorted(tag_keys.items(), key=lambda item: item[1], reverse=True)]
        print(count, tags)
        for el in stag[:15]:
            print(el)

        scities = [[k, v] for k, v in sorted(cities.items(), key=lambda item: item[1], reverse=True)]
        # print(count, scities)
        with open('cities.txt', 'w') as file:
            for el in scities:
                print(el[0], el[1], file=file)
                cities_list.append(el[0])

        sstreets = [[k, v] for k, v in sorted(streets.items(), key=lambda item: item[1], reverse=True)]
        with open('streets.txt', 'w') as file:
            for el in sstreets:
                print('{}\t{}'.format(el[0], el[1]), file=file)
                data = el[0].split('\t')
                city = data[0]
                street = data[1]
                if(street+city) not in seen_streets:
                    all_streets.append({'city': city, 'street': street, 'locations': locations[street]})
                    seen_streets.add(street+city)
                

    if event == 'end' and elem.tag in ['node', 'way', 'relation']:
        elem.clear()
    count += 1
    if count>31110000:
        break

cities_list = list(set(cities_list))
for i in cities_list:
    all_cities.append({'name' : i})

cities_collection.insert_many(all_cities)
streets_collection.insert_many(all_streets)

for street in all_streets:

    is_in_range = False

    if(street['city'] == 'Thessaloniki' or street['city'] == 'Θεσσαλονίκη'):
        if len(street['locations']) > 0:
            for location in street['locations']:
                test_point = {'lat': float(
                    location['lat']), 'lon': float(location['lon'])}
                if test_point['lat'] >= se_point['lat'] and test_point['lon'] <= se_point ['lon'] and test_point['lat'] <= nw_point ['lat'] and test_point['lon'] >= nw_point['lon']:
                    is_in_range = True
    if is_in_range:
        print(street)
        found_streets.append(
            {'city': street['city'], 'street': street['street']})



with open('result.json', 'w') as file:
    json.dump(found_streets, file)