'''
OSM Files can be found at
https://github.com/xyjprc/hon/tree/master/data_porto_taxi/porto_portugal.osm2pgsql-geojson
'''

import json
import os,sys

## TODO: directly use streets as locations

poi_file_path = sys.path[0]+'/porto_portugal_osm_point.geojson'
poi_file = open(poi_file_path)

poi_locations = []
loc_categories = {}
excluded_types = [None, 'atm','bench','charging_station','clock','compressed_air','drinking_water','elevator','public_bookcase','post_box','recycling','shower','traffic_signals','Tintas','vending_machine','waste_disposal','waste_basket']
category_types = ['police']

for poi_line in poi_file:
	j = json.loads(poi_line[:-2])
	type = j["properties"]['amenity']
	lat = j['geometry']['coordinates'][0]
	lon = j['geometry']['coordinates'][1]
	id_osm = str(int(j['properties']['osm_id']))
	if j["properties"]['amenity'] not in excluded_types:
		poi_locations.append([id_osm,str(type),float(lat),float(lon)])
	if j["properties"]['amenity'] in category_types:
		loc_categories[(float(lon), float(lat))] = str(id_osm)
poi_file.close()
print "Nb loc = "+str(len(poi_locations))

## Look for the location categories closest to coord [lon,lat]
def CoordToCat(lon, lat):
	min = 999
	closest = -1
	for plon, plat in loc_categories:
		distance = (plon-lon)**2 + (plat-lat)**2
		if distance < min:
			closest = loc_categories[(plon, plat)]
			min = distance
	return closest

## Find the category of each location (closest POI of any type in category_types)
for i in range(len(poi_locations)):
	dat_loc = poi_locations[i]
	lon, lat = dat_loc[3], dat_loc[2]
	cat = CoordToCat(lon, lat)
	dat_loc.append(cat)
	poi_locations[i] = dat_loc

## Export locations
export_locations_path = sys.path[0]+'/poi_locations.csv'
export_locations_file = open(export_locations_path,mode='w')
# export_locations_file.write('id,osm_id,type,long,lat\n')
for i in range(len(poi_locations)):
	w_line = [str(i+1)]
	w_line.extend([str(v) for v in poi_locations[i]])
	export_locations_file.write(','.join(w_line)+'\n')
export_locations_file.close()
