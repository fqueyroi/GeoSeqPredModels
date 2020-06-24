import os
import IOUtils
################################################################################
def getSequences(min_length = 2):
	'''
	Load Taxi trips in file reported in file trajectories_amenity.csv
	with a length of at least min_length.
	Note: if DataModUtils.removeRepetitions is called on the results
		  some sequences may be of length < min_length
	'''
	filepath_traces  = os.path.dirname(__file__)+'/Porto_Taxis/trajectories_amenity.csv'
	temp_seqs = IOUtils.readFile(filepath_traces)
	sequences = []
	for s in temp_seqs:
		if len(s)>=min_length:
			sequences.append(s)
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

# print len(getSequences())
# print len(getLocations())
# print getCategories()
