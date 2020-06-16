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

def getCategories():
    locations_file_path = os.path.dirname(__file__)+'/Lloyds_maritime/table_places.csv'
    categories = IOUtils.getCategories(locations_file_path, 4, 5)
    return categories

################################################################################

def filterAlphabet(alphabet, categories):
	filtered_alp = []
	for i in alphabet:
		if i in categories:
			filtered_alp.append(i)
	return filtered_alp
################################################################################

def filterSequences(sequences, categories):
	filtered_seq = []
	valid=True
	for i in range(len(sequences)):
		for j in range(len(sequences[i])):
			if sequences[i][j] not in categories:
				valid =False
		if valid == True:
			filtered_seq.append(sequences[i])
	return filtered_seq



# sequences = getSequences()
# categories = getCategories()
# print sequences
# print categories
# print getLocations()
# print filterSequences(sequences, categories)


