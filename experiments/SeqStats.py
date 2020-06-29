import numpy as np
import math

################################################################################
def symbols(sequences):
	symbols = set()
	for i in range(len(sequences)):
		seq = sequences[i]
		for s in seq :
			symbols.add(s)
	return symbols

################################################################################
def numberOfSymbols(sequences):
	return len(symbols(sequences))

################################################################################
def str_probs(probs):
	h_probs = []
	for p in probs:
		h_probs.append(round(p*100.,2))
	return str(h_probs)

################################################################################
def lengthDistribution(sequences, bins = [2,3,4,5,10,20,50]):
	lengths = [len(s) for s in sequences]
	if max(lengths) > bins[-1]:
		bins.append(max(lengths))
	return np.histogram(lengths,bins=bins)[0]

################################################################################
def lengthsSummary(sequences):
	lengths = [len(s) for s in sequences]
	min_l = min(lengths)
	max_l = max(lengths)
	mean_l = sum(lengths)/ (len(sequences) + 0.)
	return min_l,mean_l,max_l

################################################################################
def entropy(seq):
	n = len(seq)
	if n <= 1:
		return 0.
	value,counts = np.unique(seq, return_counts=True)
	probs = counts / (n + 0.)

	ent = 0.
	# Compute entropy
	for i in probs:
		ent -= i * math.log(i, 2)
	return ent

################################################################################
def entropySummary(sequences):
	nb_sym = numberOfSymbols(sequences)
	theo_max_e = -math.log(1./(nb_sym + 0.),2)
	entropies = []
	for s in sequences:
		entropies.append(entropy(s))
	min_e = min(entropies) / theo_max_e
	max_e = max(entropies) / theo_max_e
	mean_e = sum(entropies)/ (theo_max_e*len(sequences))
	return min_e,mean_e,max_e

################################################################################
def categoriesDistribution(categories, bins='auto'):
	'''
	Input:
	------
	category: dict symbol -> category of the symbol
	'''
	value,c_sym = np.unique(categories.values(), return_counts=True)
	hist_c, t_bins = np.histogram(c_sym,bins='auto')
	r_bins = [int(math.floor(v)) for v in t_bins]
	return hist_c, r_bins

################################################################################

import sys, os
import DataModUtils
sys.path.append(''.join([os.path.dirname(__file__), '/..', '/data/']))
import LoadAirportsData
import LoadLlyodsData
import LoadPortoTaxisData

# sequences = LoadAirportsData.getSequences()
# categories = LoadAirportsData.getCategories()
# sequences = LoadPortoTaxisData.getSequences()
# categories = LoadPortoTaxisData.getCategories()
# sequences = LoadLlyodsData.getSequences()
# categories = LoadLlyodsData.getCategories()
#
# sequences = DataModUtils.removeRepetitions(sequences)
#
# nb_seq =  len(sequences)
# nb_sym =  numberOfSymbols(sequences)
# sum_l = [str(round(v,2)) for v in lengthsSummary(sequences)]
# sum_e = [str(round(v,2)) for v in entropySummary(sequences)]
# bins = [0,2,3,4,5,10,20,50]
# hist = [str(v) for v in lengthDistribution(sequences,bins)]
# output_v = [str(nb_seq),str(nb_sym)] + sum_l + sum_e + hist
#
# name_bins = ','.join(['h'+str(b) for b in bins])
# print "nb_seq,nb_sym,min_l,mean_l,max_l,min_e,mean_e,max_e,"+name_bins
# print ','.join(output_v)
#
# nb_cat = len(set(categories.values()))
# print nb_cat
# nb_sym = len(categories.keys())
# print nb_sym
# hist_c, bins_c = categoriesDistribution(categories)
# print hist_c
# print bins_c
