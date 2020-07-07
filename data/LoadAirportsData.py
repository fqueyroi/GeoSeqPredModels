import os
import IOUtils
################################################################################
def getSequences():
	filepath_traces  = os.path.dirname(__file__)+'/DB1BAirports/2011Q1_SEQ.csv'
	sequences = IOUtils.readFile(filepath_traces,True,sep=',')
	return sequences

################################################################################
def getCategories():
	categories_file_path   = os.path.dirname(__file__)+'/DB1BAirports/2011Q1_AIRPORTS.csv'
	categories = IOUtils.getCategories(categories_file_path,0,2,sep=',',header=False)
	return categories

################################################################################
def getLocations():
	locations_file_path   = os.path.dirname(__file__)+'/DB1BAirports/MASTER_CORD.csv'
	# locations = IOUtils.readLocations(locations_file_path,0,1,2,sep=',',header=False)
	locations = IOUtils.readLocations(locations_file_path,0,1,2,sep=',',header=True)
	return locations
################################################################################


# sequences = getSequences()
# print len(sequences)
# print sequences[0]
# categories = getCategories()
# print len(categories)
# print categories
# locations = getLocations()
# print len(locations)
# print locations
