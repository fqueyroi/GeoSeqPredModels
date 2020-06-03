# -*- coding: utf-8 -*-
""" Base inferface for Location-Based Sequence generator
GeoFixOrderModel should perform better for this generator
"""
import SequenceGenerator
import random
import math

def dist(p1,p2):
	return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def rbf_kernel(p1, p2, sigma):
	d = dist(p1, p2)
	rbf = math.exp(- (d/math.sqrt(2.))**2 / sigma)
	return rbf

class LocationBasedGenerator(SequenceGenerator.SequenceGenerator):

	def __init__(self, alphabet_size = 100, stop_prob = 0.1,sigma = 0.0001):
		'''
		Parameters:
		-----------
		alphabet_size: int
			Size of the underlying network use to generate the sequences
		stop_prob: float [0,1]
			Probability to stop a sequence during its generation
		sigma: float > 0
			Preference for far locations
			(0: we stay on the same locations,
			infinity: all locations have the same probability to be picked)
		'''
		self.alphabet_size = alphabet_size
		self.stop_prob = stop_prob
		self.locations = {} ## alphabet elem -> random [x,y] in [0,1]
		self.sigma = sigma
		self.generateLocations()

	def generateLocations(self):
		### locations are in the [0,1] square
		for i in range(self.alphabet_size):
			self.locations[str(i)] = [random.random(),random.random()]

	def nextSymbol(self, context=[]):
		'''
		Pick a locations according to the given 'context'
		2 possibilies:
			- empty context: a location picked at random
			- one previous locations: a location is picked around the previous
			  one (depending on the value of 'self.sigma')
		'''
		if len(context)==0:
			return random.randint(0,self.alphabet_size-1)
		if len(context)==1:
			pc = self.locations[str(context[0])]
			sum_d = 0.
			for i in range(self.alphabet_size):
				pi = self.locations[str(i)]
				sum_d += rbf_kernel(pc,pi,self.sigma)

			u = random.random()
			cp = 0.
			for i in range(self.alphabet_size):
				pi = self.locations[str(i)]
				prox = rbf_kernel(pc,pi,self.sigma)
				cp += prox/sum_d
				if cp >= u:
					return i
			return -1

	def generate(self, nb_seq):
		'''
		The sequences generated are of size <= 2 * self.alphabet_size
		'''
		sequences = []
		for n in range(nb_seq):
			context = []
			seq = []
			stop = False
			while not stop:
				next_s = self.nextSymbol(context)
				seq.append(str(next_s))
				context = [next_s]
				if (len(seq)>2 and random.random() < self.stop_prob):
					stop=True
				if len(seq) > 2.*self.alphabet_size:
					stop=True
			sequences.append(seq)
		return sequences


# gen = LocationBasedGenerator(alphabet_size = 20, stop_prob = 0.1,sigma = 0.01)
# sequences = gen.generate(10)
# for s in sequences:
# 	print s
