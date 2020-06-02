'''
OSM Files can be found at
https://github.com/xyjprc/hon/tree/master/data_porto_taxi/porto_portugal.osm2pgsql-geojson
'''

import json
import os,sys

## TODO directly use streets as locations

poi_locations = []
poi_file_path = sys.path[0]+'/porto_portugal_osm_point.geojson'
poi_file = open(poi_file_path)
excluded_types = [None, 'atm','bench','charging_station','clock','compressed_air','drinking_water','elevator','public_bookcase','post_box','recycling','shower','traffic_signals','Tintas','vending_machine','waste_disposal','waste_basket']

for poi_line in poi_file:
	j = json.loads(poi_line[:-2])
	type = j["properties"]['amenity']
	if j["properties"]['amenity'] not in excluded_types:
		id_osm = str(int(j['properties']['osm_id']))
		lat = j['geometry']['coordinates'][0]
		lon = j['geometry']['coordinates'][1]
		poi_locations.append([id_osm,str(type),str(lat),str(lon)])
poi_file.close()
print "Nb loc = "+str(len(poi_locations))

export_locations_path = sys.path[0]+'/poi_locations.csv'
export_locations_file = open(export_locations_path,mode='w')
# export_locations_file.write('id,osm_id,type,long,lat\n')
for i in range(len(poi_locations)):
	w_line = [str(i+1)]
	w_line.extend(poi_locations[i])
	export_locations_file.write(','.join(w_line)+'\n')
export_locations_file.close()
