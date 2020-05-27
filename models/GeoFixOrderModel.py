# -*- coding: utf-8 -*-
""" Base class for Geographical Fixed order prediction model
"""

import PredModel
import math


def LongLatDist(p1,p2) :
	### Distance (in km) between locations p1 and p2
	### using Haversine formula
	r1 = (math.radians(p1[1]),math.radians(p1[0]))
	r2 = (math.radians(p2[1]),math.radians(p2[0]))
	d_long = (r2[0] - r1[0])
	d_latt = (r2[1] - r1[1])
	a = math.sin(d_latt/2)**2 + math.cos(r1[1]) * math.cos(r2[1]) * math.sin(d_long/2)**2
	c = 2 * math.asin(math.sqrt(a))
	return 6371 * c

def EucliDist(p1,p2) :
	return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]))

def rbfAtPosition(pos, center, sigma, M, dist_fun = EucliDist):
	dist = dist_fun(pos, center)
	rbf = math.exp(- (dist/M) * (dist/M) / sigma)
	return rbf

class GeoFixOrderModel(PredModel.PredModel):
	""" Model of order-k for Geo-localized Sequence prediction
	Estimate the distribution of points occuring after sequences of
	length less than k
	"""

	def __init__(self, maxContextLength, alphabet, locations, sigma, dist_fun = EucliDist):
		'''
		Parameters:
		-----------
		locations: dict: alphabet -> [float,float]
			position of points in the alphabet

		sigma: float > 0
			Spread for the RDF Kernel
			if close to 0 : results close to the FixOrderModel
			if very large : uniform probabilities

		dist_fun: function
			Used to compute distance between locations p1 and p2
			with p1 and p2 being [float,float]
		'''
		super(GeoFixOrderModel, self).__init__(maxContextLength, alphabet)
		self.locations = locations ## alphabet label -> [lat, long]
		self.sigma = sigma
		self.dist_fun = dist_fun

		# self.max_d = 0.
		# for p1 in self.locations.values():
		# 	for p2 in self.locations.values():
		# 		d = self.dist_fun(p1, p2)
		# 		self.max_d = max(self.max_d,d)
		# print "Max D = "+str(self.max_d)
		self.max_d = 1.
		## TODO: find if to use dist / max(dist)

		## TODO: improve computation time somehow ?
		self.sum_d = dict() ## alphabet-> float

		for s1 in self.alphabet:
			self.sum_d[s1] = 0.
			if s1 in self.locations.keys():
				p1 = self.locations[s1]
				for s2 in self.alphabet:
					if s2 in self.locations.keys():
						p2 = self.locations[s2]
						rbf = rbfAtPosition(p2,p1,self.sigma, self.max_d, self.dist_fun)
						self.sum_d[s1] += rbf

	def learn(self, seq):
		super(GeoFixOrderModel, self).learn(seq)

	def prune(self):
		## TODO: not exactly pruning -> should change PredModel.prune() name
		## to postProcressing()
		self.recurComputeDensities(self.tree)


	def recurComputeDensities(self, node):
		cur_dens = dict()
		for sym in self.alphabet:
			cur_dens[sym] = 0.
			if sym in self.locations.keys():
				cur_dens[sym] = self.densityAtPosition(self.locations[sym], node)
		self.densities[node.symbol] = cur_dens

		for k, c in node.children.iteritems():
			self.recurComputeDensities(c)

	def densityAtPosition(self, pos, node):
		dens = 0.
		n = node.totalCount() + 0.
		for sym, c in node.counts.iteritems():
			if sym in self.locations.keys():
				pos_sym = self.locations[sym]
				dist = self.dist_fun(pos,pos_sym)
				rbf = math.exp(- (dist/self.sigma)*(dist/self.sigma) / 2. )
				dens = dens + c/n * rbf
		return dens

	def probability(self, symbol, context):
		if symbol not in self.locations.keys():
			return 0.
		p_sym = self.locations[symbol]

		context_node = self.tree.longestPrefix(context)

		d_sym = 0.
		sum_dens = 0.
		n = context_node.totalCount() + 0.
		for k, c in context_node.counts.iteritems():
			if k not in self.locations.keys():
				continue
			p_k = self.locations[k]
			d_sym += (c/n) * rbfAtPosition(p_sym, p_k, self.sigma, self.max_d, self.dist_fun)
			sum_dens += (c/n) * self.sum_d[k]

		if sum_dens == 0:
			return 0.
		return d_sym / sum_dens

	def __str__(self):
		res = "Geo-Fixed-Order Model("
		res += str(self.maxContextLength)
		res += ","
		res += str(self.sigma)
		res += ")"
		return res


# seq = ''.join(['aaacgt' for i in range(30)])
# alphabet = ['a','c','g','t']
# locations = {'a' : [0.,0.], 'c' : [-1.,-1.], 'g' : [3.2,3.2], 't' : [3.,3.]}
# print seq
# print locations
#
# model = GeoFixOrderModel(3, alphabet, locations, .1, EucliDist)
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
