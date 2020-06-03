# -*- coding: utf-8 -*-
"""
Scale-free model with returns mecanic
ThereAndBackModel should perform best for this
"""

import SequenceGenerator
from collections import Counter
import random

class HierarchicalReturnGenerator(SequenceGenerator.SequenceGenerator):

	def __init__(self, alphabet_size = 100, k = 3, stop_prob = 0.1, prob_return_node = 0.3):
		'''
		Parameters:
		-----------
		alphabet_size: int
			Size of the underlying network use to generate the sequences
		k: int
			Average number of new connexion in the network
			i.e. number of edges ~= k*alphabet_size
		stop_prob: float [0,1]
			Probability to stop a sequence during its generation
		prob_return_node: float [0,1]
			Ratio of return node in the network i.e. nodes for which
			the next node visited is the previous one
		'''
		self.alphabet_size = alphabet_size
		self.k  = k
		self.network = [] ## list port -> adjacency list of alphabet elements
		self.stop_prob = stop_prob
		self.prob_return_node = prob_return_node
		self.max_deg = 0
		self.return_nodes = []
		self.generateNetwork()

	def generateNetwork(self):
		self.network = []
		## Init the network with k nodes all connected together
		for i in range(self.k):
			adj = range(self.k)
			del adj[i]
			self.network.append(adj)
		## Add self.alphabet_size - self.k new nodes
		for i in range(self.k, self.alphabet_size):
			adj = random.sample(range(i),self.k)
			for o in adj:
				self.network[o].append(i)
				## update max_deg
				self.max_deg = max(self.max_deg,len(self.network[o]))
			self.network.append(adj)
		## Pick the 'return nodes'
		for i in range(self.alphabet_size):
			if random.random() < self.prob_return_node:
				self.return_nodes.append(i)

	def generate(self, nb_seq):
		'''
		The sequences generated are of size <= 2 * self.alphabet_size
		'''
		sequences = []
		for i in range(nb_seq):
			seq = []
			self.randomWalk(seq)
			sequences.append(seq)
		return sequences

	def randomWalk(self, cur_seq = []):
		'''
		Recursively build the sequences 'cur_seq'
		'''
		if len(cur_seq) == 0:
			cur_seq.append(random.randint(0, self.alphabet_size - 1))
			self.randomWalk(cur_seq)
			return
		if len(cur_seq) > 1 :
			if random.random() < self.stop_prob or len(cur_seq) >= 2*self.alphabet_size:
				return
			else:
				cur_n = cur_seq[-1]
				if cur_n in self.return_nodes:
					cur_seq.append(cur_seq[-2])
					self.randomWalk(cur_seq)
					return
		cur_n = cur_seq[-1]
		o = random.choice(self.network[cur_n])
		cur_seq.append(o)
		self.randomWalk(cur_seq)


# gen = HierarchicalReturnGenerator(50, 3, 0.15, 0.4)
# print "Size network : " + str(len(gen.network))
# for i in range(len(gen.network)):
# 	print "Port "+str(i)+" : "+str(len(gen.network[i]))
# 	# for o in gen.network[i] :
# 	# 	print "	-> "+ str(o)
# print "Return nodes : "+str(gen.return_nodes)
# print
#
# sequences = gen.generate(5)
# for seq in sequences:
# 	print seq
