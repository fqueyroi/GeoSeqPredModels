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
# sequences = getSequences()
# print len(sequences)
# print sequences[0]
# # print len(getLocations())
# categories = getCategories()
# print len(categories)
# print categories
