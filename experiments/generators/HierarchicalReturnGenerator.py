# -*- coding: utf-8 -*-
""" Base inferface for Hierarchical geographical sequence generation
Scale-free model with returns mecanic
"""

import SequenceGenerator
from collections import Counter
import random

class HierarchicalReturnGenerator(SequenceGenerator.SequenceGenerator):

	def __init__(self, nb_ports = 100, k = 3, stop_prob = 0.1, prob_return_node = 0.3):
		self.nb_ports = nb_ports
		self.k  = k
		self.network = [] ## list port -> adjacency list of ports index
		self.stop_prob = stop_prob
		self.prob_return_node = prob_return_node
		self.max_deg = 0
		self.return_nodes = []
		self.generateNetwork()

	def generateNetwork(self):
		self.network = []
		for i in range(self.k):
			adj = range(self.k)
			del adj[i]
			self.network.append(adj)

		for i in range(self.k, self.nb_ports):
			adj = random.sample(range(i),self.k)
			for o in adj:
				self.network[o].append(i)
				## update max_deg
				self.max_deg = max(self.max_deg,len(self.network[o]))
			self.network.append(adj)

		for i in range(self.nb_ports):
			if random.random() < self.prob_return_node:
				self.return_nodes.append(i)

	def generate(self, nb_seq, filename, sep = ' '):
		sequences = []
		for i in range(nb_seq):
			seq = []
			self.randomWalk(seq)
			sequences.append(seq)
		self.write(sequences, filename, sep)

	def randomWalk(self, cur_seq = []):
		if len(cur_seq) == 0:
			cur_seq.append(random.randint(0, self.nb_ports - 1))
			self.randomWalk(cur_seq)
			return
		if len(cur_seq) > 1 :
			if random.random() < self.stop_prob or len(cur_seq) >= 2*self.nb_ports:
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


gen = HierarchicalReturnGenerator(100, 4, 0.15, 0.4)
print "Nb ports : " + str(len(gen.network))
for i in range(len(gen.network)):
	print "Port "+str(i)+" : "+str(len(gen.network[i]))
	# for o in gen.network[i] :
	# 	print "	-> "+ str(o)
print "Return nodes : "+str(gen.return_nodes)
print

filename = "/home/queyroi-f/cs/HighOrderNetworks/dev/VOM_algorithms/NonArithmeticPPMC/generators/test_return.csv"
gen.generate(1000, filename, sep = ' ')

# nb_seq = 1000
# dist_len_seq = Counter()
# for i in range(nb_seq):
# 	seq = []
# 	gen.randomWalk(seq)
# 	# print seq
# 	dist_len_seq[len(seq)]+=1

# max_len = max(dist_len_seq.keys())
#
# for i in range(2, max_len + 1):
# 	str_c = ''
# 	for j in range(dist_len_seq[i]):
# 		str_c += '#'
# 	print str(i)+ " : "+str_c
