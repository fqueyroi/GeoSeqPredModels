'''
using parts of
https://github.com/xyjprc/hon/blob/master/data_porto_taxi/CleanPortugalData.py
'''

from collections import defaultdict
import datetime
from datetime import date
import csv

import os,sys

train_file_path = sys.path[0]+'/train.csv'
poi_file_path = sys.path[0]+'/poi_locations.csv'
## taking first day
max_date = date(2013,7,1) ## min date is date(2013,6,30)

output_file_path = sys.path[0]+'/trajectories_amenity.csv'

## Load POI locations
pois = {}
with open(poi_file_path) as f:
	for line in f:
		# 'id,osm_id,type,long,lat\n'
		fields = line.strip().split(',')
		lon, lat, id = fields[3], fields[4], fields[0]
		pois[(float(lon), float(lat))] = str(id)

## Look for the POI closest to coord [lon,lat]
def CoordToPOI(lon, lat):
	min = 999
	closest = -1
	for plon, plat in pois:
		distance = (plon-lon)**2 + (plat-lat)**2
		if distance < min:
			closest = pois[(plon, plat)]
			min = distance
	return str(closest)

## Convert polyne to sequence of POIS
def PolylineToGrid(polyline):
	#print(polyline)
	vals = []
	polyline = polyline.split(']')
	for pair in polyline:
		p = pair
		if len(p) < 2:
			continue
		if pair[0] == ',':
			p = pair[2:]
		lon = float(p.split(',')[0].replace('[', '').replace(']', ''))
		lat = float(p.split(',')[1].replace('[', '').replace(']', ''))
		if -9 < lon < -8 and 40 < lat < 42:
			vals.append(CoordToPOI(lon, lat))
	return vals

### Load Taxi data traces
print "Reading Taxi traces"
final_traces = [] ## id + traces
with open(train_file_path) as f:
	counter = 0
	reader = csv.reader(f)
	next(f)
	for row in reader:
		counter += 1
		if counter % 100 == 0:
			print(counter)
		TRIP_ID,CALL_TYPE,ORIGIN_CALL,ORIGIN_STAND,TAXI_ID,TIMESTAMP,DAY_TYPE,MISSING_DATA,POLYLINE=row
		trip_date = datetime.datetime.utcfromtimestamp(int(TIMESTAMP)).date()
		if trip_date > max_date:
			break
		if MISSING_DATA=='False' :
			poids_traces = [str(TAXI_ID)]
			poids_traces.extend(PolylineToGrid(POLYLINE))
			# print trip_date
			# print " "+str(POLYLINE)
			# print " "+str(poids_traces)
			# print
			final_traces.append(poids_traces)

## Output final traces
print "Writing output"
output_file = open(output_file_path, 'w')
for trace in final_traces:
	output_file.write(trace[0] + ' ' + ' '.join(trace[1:]) + '\n')

# ## Sort according to timestamp
# print "Sorting Taxi Traces"
# raw_taxi_data.sort()

## Merge traces according to the week and the Taxi Id
# print "Merge Traces"
# trips = defaultdict(lambda: defaultdict(list))
# counter = 0
# for line in raw_taxi_data:
# 	counter += 1
# 	if counter % 10000 == 0:
# 		print(counter)
# 	TIMESTAMP = line[0]
# 	TAXI_ID, POLYLINE = line[1]
# 	TripDate = datetime.datetime.utcfromtimestamp(int(TIMESTAMP)).date()
# 		TripWeek = (TripDate-date(2013,6,30)).days//7
# 	trips[TripWeek][TAXI_ID].extend(PolylineToGrid(POLYLINE))

## Output trips by week
# print "Writing output"
# for TripWeek in trips:
# 	with open(traj_folder_name + str(TripWeek) +'.csv', 'w') as f:
# 		print(TripWeek)
# 		for TAXI_ID in trips[TripWeek]:
# 			f.write(TAXI_ID + ' ' + ' '.join(trips[TripWeek][TAXI_ID]) + '\n')
