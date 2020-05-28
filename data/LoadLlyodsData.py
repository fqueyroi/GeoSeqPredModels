import os
import IOUtils
################################################################################
def getSequences():
	filepath_traces  = os.path.dirname(__file__)+'/Lloyds_maritime/apr2009_oct2009/portseq_apr2009_oct2009.csv'
	sequences = IOUtils.readFile(filepath_traces)
	return sequences
################################################################################
def getLocations():
	locations_file_path   = os.path.dirname(__file__)+'/Lloyds_maritime/table_places.csv'
	locations = IOUtils.readLocations(locations_file_path,4,6,7)
	return locations
################################################################################
# print len(getSequences())
# print getLocations()
