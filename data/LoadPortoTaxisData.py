import os
import IOUtils
################################################################################
def getSequences(all_weeks = True, week = 0):
	filepath_traces  = os.path.dirname(__file__)+'/Porto_Taxis/trajectories_amenity.csv'
	sequences = IOUtils.readFile(filepath_traces)

	# dir_traces  = os.path.dirname(__file__)+'/Porto_Taxis/trajectories/'
	# list_traces = []
	# if all_weeks:
	# 	list_traces = [dir_traces+'/'+f for f in os.listdir(dir_traces) if os.path.isfile(os.path.join(dir_traces, f))]
	# else:
	# 	week_traces_file = dir_traces+str(week)+'.csv'
	# 	list_traces.append(week_traces_file)
	#
	# sequences = []
	# for file_path in list_traces:
	# 	temp_sequences = IOUtils.readFile(file_path)
	# 	sequences += temp_sequences
	return sequences
################################################################################
def getLocations():
	locations_file_path   = os.path.dirname(__file__)+'/Porto_Taxis/poi_locations.csv'
	# locations = IOUtils.readLocations(locations_file_path,0,1,2,sep=',',header=False)
	locations = IOUtils.readLocations(locations_file_path,0,3,4,sep=',',header=False)
	return locations
################################################################################
def getCategories():
	locations_file_path = os.path.dirname(__file__)+'/Porto_Taxis/poi_locations.csv'
	categories = IOUtils.getCategories(locations_file_path,0,2,sep=',',header=False)
	return categories

################################################################################

# print len(getSequences(True, 0))
# print len(getLocations())
# print getCategories()