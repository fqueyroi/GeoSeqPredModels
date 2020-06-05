# -*- coding: utf-8 -*-
""" Base inferface for Sequence prediction models.
	All instance rely on a suffix tree to count the number of
	sequences up to a given length (class member "maxContextLength")
	for a given alphabet (class member "alphabet")
"""
## TODO: write a model that use known categories about symbols (countries, continent etc.) 

import SuffixTree as trie

class PredModel(object):
	"""Abstract class for Prediction models"""

	def __init__(self, maxContextLength, alphabet):
		""" Initialize the PPC-Model
		Parameters:
		-----------
		maxContextLength: int
			The maximum length of context
		alphabet: list of str
			Possible values to predict
		"""
		self.maxContextLength = maxContextLength
		self.alphabet = alphabet
		self.tree = trie.SuffixNode('', None, 0)  ## root node with dummy symbol


	def learn(self, seq):
		""" Use to the sequence 'seq' to train the model
		Parameters:
		-----------
		seq: list of str
			The sequence of symbols to use
		"""
		## TODO this is a mess
		if len(seq) == 0:
			## does nothing
			return
		if len(seq) == 1:
			## only add seq[0] to the base counter
			self.tree.increment(seq[0],[])
			return
		if len(seq) <=  self.maxContextLength:
			self.tree.increment(seq[0],[])
			for i in range(2,len(seq) + 1):
				cseq = seq[:i]
				self.tree.increment(cseq[-1],cseq[:-1])
		else:
			maxlength = self.maxContextLength
			self.tree.increment(seq[0],[])
			for i in range(2,maxlength + 1):
				cseq = seq[:i]
				self.tree.increment(cseq[-1],cseq[:-1])
			for i in range(len(seq) - maxlength) :
				length = min(maxlength + 1, len(seq) - i)
				cseq = seq[i:i+length]
				self.tree.increment(cseq[-1],cseq[:-1])

	def prune(self):
		'''
		Remove redundant paths in the tree.
		Depends on the actual model used.

		'''
		pass

	def size(self):
		'''
		Computes the size of the models (its "complexity")
		'''
		return self.tree.numberOfNodes()

	def probability(self, symbol, context = []):
		""" Returns the estimated probability
		of observing 'symbol' after the sequence 'context'
		according to the model
		Parameters:
		-----------
		symbol: str
			The symbol whose probability is to be computed
		context: list of str
			The sequence of symbol used for prediction

		Returns:
		--------
		prob: float
			The conditional probability of observing 'symbol'

		Warning:
		--------
		If len(context) > self.maxContextLength the model will only
		the last self.maxContextLength elements of 'context'
		"""
		pass

	def randomSymbol(self, context = []):
		"""
		Returns a symbol of the alphabet at random
		using probability given by the context
		"""
		import random
		u = random.random()
		cum_p = 0.
		for a in self.alphabet:
			cum_p += self.probability(a, context)
			if cum_p >= u:
				return a

	def probabilites(self, sequence, context = []):
		""" Returns the estimated probabilities
		of observing the given 'sequence' after the sequence 'context'
		according to the model
		Parameters:
		-----------
		sequence: list of str
			The sequence whose probability is to be computed
		context: list of str
			The sequence of symbol used for prediction
			note: can be empty

		Returns:
		--------
		probs: list of float
			The conditional probability of observing each symbol
			of 'sequence'

		Warning:
		--------
		If len(context) > self.maxContextLength the model will only
		the last self.maxContextLength elements of 'context'
		"""
		probs = [0 for i in range(len(sequence))]
		temp_context = context[:]
		for i in range(len(sequence)):
			probs[i] = self.probability(sequence[i],temp_context)
			temp_context.append(sequence[i])
		return probs

	def averageLogLoss(self, sequence, context = []):
		""" For a sequences S=(x_1,x_2,...) of length T returns
		the average average LogLoss i.e.

		- sum_i^{T} log_2(probability(x_i | context + x_1...x_{i-1}))

		Ref:
		See Eq. 1 in
		Begleiter et al., "On Prediction Using Variable Order Markov Models"
		Journal of Artificial Intelligence Research, 22, (2004), 385-421

		Parameters:
		-----------
		sequence: list of str
			The sequence whose probability is to be computed
		context: list of str
			The sequence of symbol used for prediction
			note: can be empty

		Returns:
		--------
		logloss: float
			the average log-loss (in bits)
		"""
		import math
		probs = self.probabilites(sequence, context)
		logloss = 0.
		for p in probs:
			logloss -= math.log(p,2)
		logloss /= len(sequence) + 0.
		return logloss
