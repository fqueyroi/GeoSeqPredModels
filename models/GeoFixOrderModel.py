# -*- coding: utf-8 -*-
""" Base class for Geographical Fixed order prediction model
"""

from enum import Enum

import PredModel
import math


def LongLatDist(p1,p2) :
	### Distance (in km) between locations p1 and p2
	### using Haversine formula
	r1 = (math.radians(p1[0]),math.radians(p1[1]))
	r2 = (math.radians(p2[0]),math.radians(p2[1]))
	d_long = (r2[0] - r1[0])
	d_latt = (r2[1] - r1[1])
	a = math.sin(d_latt/2)**2 + math.cos(r1[1]) * math.cos(r2[1]) * math.sin(d_long/2)**2
	c = 2 * math.asin(math.sqrt(a))
	return 6371 * c

def EucliDist(p1,p2) :
	return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

class DistCalc(Enum):
	EUCLIDIAN = 1
	HAVERSINE = 2
Dists = {DistCalc.EUCLIDIAN: EucliDist, DistCalc.HAVERSINE: LongLatDist}

def rbf(pos, center, gamma, M, dist_fun = DistCalc.EUCLIDIAN):
	dist = dist_fun(pos, center)
	res = math.exp(- (dist/M)**2 / gamma)
	return res

def getMaxDistance(locations, dist_fun = DistCalc.EUCLIDIAN):
	max_d = 0.
	for p1 in locations.values():
		for p2 in locations.values():
			d = dist_fun(p1, p2)
			max_d = max(max_d,d)
	return max_d

def sumDensities(alphabet, locations, gamma, max_d, dist_fun = DistCalc.EUCLIDIAN):
	sum_d = dict() ## alphabet-> float
	for s1 in alphabet:
		sum_d[s1] = 0.
		if s1 in locations.keys():
			p1 = locations[s1]
			for s2 in alphabet:
				if s2 in locations.keys():
					p2 = locations[s2]
					sum_d[s1] += rbf(p2, p1, gamma, max_d, dist_fun)
	return sum_d


class GeoFixOrderModel(PredModel.PredModel):
	""" Model of order-k for Geo-localized Sequence prediction
	Estimate the distribution of points occuring after sequences of
	length less than k
	"""

	def __init__(self, k, A, locations, gamma, dist_fun = DistCalc.EUCLIDIAN,
					max_d = 0., sum_dens = None, zero_p = False):
		'''
		Parameters:
		-----------
		locations: dict: alphabet -> [float,float]
			position of points in the alphabet

		gamma: float > 0
			Spread for the RDF Kernel
			if close to 0 : results close to the FixOrderModel
			if very large : uniform probabilities

		dist_fun: function
			Used to compute distance between locations p1 and p2
			with p1 and p2 being [float,float]

		zero_p: bool
			If True the probability of a subsequence not observed during
			training is set to zero

		'''

		super(GeoFixOrderModel, self).__init__(k, A)
		self.locations = locations ## alphabet label -> [lat, long]
		self.gamma = gamma
		self.dist_fun = dist_fun

		self.zero_p = zero_p
		self.max_d = max_d
		if max_d == 0.:
			self.max_d = getMaxDistance(self.locations, self.dist_fun)

		self.sum_d = dict()
		if not self.zero_p:
			if sum_dens is None:
				self.sum_d = sumDensities(self.alphabet, self.locations, self.gamma, self.max_d, self.dist_fun)
			else:
				self.sum_d = sum_dens
		# else:
		# 	self.node_sum_d = dict() ## store sum of densities for locations node.children


	def learn(self, seq):
		super(GeoFixOrderModel, self).learn(seq)

	def densityAtPosition(self, pos, node):
		dens = 0.
		n = node.totalCount() + 0.
		for sym, c in node.counts.iteritems():
			if sym in self.locations.keys():
				pos_sym = self.locations[sym]
				rbf = rbf(pos, pos_sym, self.gamma, self.max_d, self.dist_fun)
				dens = dens + c/n * rbf
		return dens

	def probability(self, symbol, context):
		if symbol not in self.locations.keys():
			return 0.
		p_sym = self.locations[symbol]

		context_node = self.tree.longestPrefix(context)
		n = context_node.totalCount() + 0.
		d_sym = 0.
		sum_dens = 0.
		if self.zero_p:
			if context_node[symbol]==0:
				return 0.
			## TODO: improve computation time somehow ? Maybe storing the vals of k_sum_dens in the nodes ?
			for k, c in context_node.counts.iteritems():
				# list_context = context_node.getSymbolPath()
				# list_context.append(k)
				k_sum_dens = 0.
				# if list_context not in self.node_sum_d.keys():
				p_k = self.locations[k]
				for k2, c2 in context_node.counts.iteritems():
					p_k2 = self.locations[k2]
					k_sum_dens += rbf(p_k, p_k2, self.gamma, self.max_d, self.dist_fun)
					# self.node_sum_dnode_sum_d[list_context] = k_sum_dens
				# else:
					# k_sum_dens = self.node_sum_d[list_context]
				sum_dens += (c/n) * k_sum_dens
				d_sym += (c/n) * rbf(p_sym, p_k, self.gamma, self.max_d, self.dist_fun)
		else:
			for k, c in context_node.counts.iteritems():
				## TODO make sure every elem as a location entry to avoid this test
				## Consider it as missing values if not
				if k not in self.locations.keys():
					continue
				p_k = self.locations[k]
				d_sym += (c/n) * rbf(p_sym, p_k, self.gamma, self.max_d, self.dist_fun)
				sum_dens += (c/n) * self.sum_d[k]

		if sum_dens == 0:
			return 0.
		return d_sym / sum_dens


	def size(self):
		return self.tree.numberOfEntries() + len(self.sum_d)


	def __str__(self):
		res = "Geo-Fixed-Order Model("
		res += str(self.maxContextLength)
		res += ","
		res += str(self.gamma)
		res += ")"
		return res


# seq = ''.join(['aaacgt' for i in range(30)])
# seq += 'aactg'
# alphabet = ['a','c','g','t']
# locations = {'a' : [0.,0.], 'c' : [-1.,-1.], 'g' : [1.1,1.1], 't' : [1.,1.]}
# print seq
# print locations
#
# model = GeoFixOrderModel(2, alphabet, locations, .5, EucliDist, 0, None, True)
# print model
#
# model.learn(seq)
#
# print model.tree
# print
# print model.sum_d
# print
#
# sum_p = 0.
# for n in alphabet:
# 	context =  ['a','c']
# 	prob = model.probability(n,context)
# 	sum_p += prob
# 	print " "+ n + " | " + ','.join(context) + " : " + str(prob)
#
# print "Sum Prob = "+str(sum_p)
