# -*- coding: utf-8 -*-
""" Main class for Shmilovici Model
ref:
Shmilovici, Armin and Ben-Gal, Irad
"Using a VOM model for reconstructing potential coding regions in EST sequences"
Computational Statistics 22, 1, 2007, Springer. p 49--69
"""

import PredModel


class ShmiloviciModel(PredModel.PredModel):
	"""Main class for Shmilovici model"""

	def __init__(self, maxContextLength, alphabet):
		super(ShmiloviciModel, self).__init__(maxContextLength, alphabet)
		self.nbOfSymbols = len(alphabet) ## Number of symbol in the base alphabet
		self.sizeTraining = 0 ## Number of symbol used for training

	def __str__(self):
		return "Shmilovici-Model("+str(self.maxContextLength)+")"

	def learn(self, seq):
		super(ShmiloviciModel, self).learn(seq)
		for s in seq:
			if s not in self.alphabet:
				self.alphabet.add(s)

		self.sizeTraining += len(seq)

	def probabilityForSymbol(self, node, symbol):
		tot_count_n = node.totalCount() + 0.
		return (node[symbol] + .5 )/ (self.nbOfSymbols / 2. + tot_count_n)

	def divergence(self, node):
		import math
		if node.parent == None:
			return self.nbOfSymbols + 1.
		res = 0.
		for k in self.alphabet:
			p_k_n = self.probabilityForSymbol(node, k)
			p_k_p = self.probabilityForSymbol(node.parent, k)
			res += p_k_n * math.log(p_k_n / p_k_p, 2)
		return res

	def divergenceThreshold(self, node):
		import math
		return .5 * (self.nbOfSymbols + 1.) / math.log(self.sizeTraining + 1.,2)

	def prune(self):
		'''
		Remove redundant paths in the tree

		'''
		self.recurPruning(self.tree)

	def recurPruning(self, node):
		to_prune = []
		for k, c in node.children.iteritems():
			if self.recurPruning(c):
				to_prune.append(k)
		for k in to_prune:
			del node.children[k]

		if node.numberChildren() > 0:
			return False
		return self.divergence(node) <= self.divergenceThreshold(node)

	def probability(self, symbol, context):
		context_node = self.tree.longestPrefix(context)
		return self.probabilityForSymbol(context_node, symbol)

seq = ''.join(['aaacgt' for i in range(30)])
alphabet = ['a','c','g','t']
print seq

model = ShmiloviciModel(3,alphabet)

model.learn(seq)

print model.tree

for n in  alphabet:
	context =  ['a','a']
	print n + " | " + ','.join(context) + " : " + str(model.probability(n,context))
