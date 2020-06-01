import json
import os,sys

poi_locations = []
poi_file_path = sys.path[0]+'/porto_portugal_osm_point.geojson'
poi_file = open(poi_file_path)
for poi_line in poi_file:
	j = json.loads(poi_line[:-2])
	if j["properties"]['amenity'] is not None:
		id_osm = str(int(j['properties']['osm_id']))
		type = j["properties"]['amenity']
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
