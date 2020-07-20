# -*- coding: utf-8 -*-
"""Suffix Tree
"""

from collections import Counter

class SuffixNode(object):
	def __init__(self, symbol, parent, depth = 0):
		self.symbol = symbol
		self.counts  = Counter()
		self.children = {}
		self.depth = depth
		self.parent = parent

	def numberOfNodes(self):
		'''
		Return the number of nodes in the tree (recursive)
		'''
		res = 1
		for k,v in self.children.iteritems():
			res += v.numberOfNodes()
		return res

	def numberOfEntries(self):
		'''
		Return the total number of entries of self.counts
		in the tree (recursive)
		'''
		res = len(self.counts)
		for k,v in self.children.iteritems():
			res += v.numberOfEntries()
		return res
	
	def longestPrefix(self, seq):
		'''
		Return the node in the subtree whose symbol path is
		the longest prefix of seq (recursive)
		'''
		if len(seq)==0 or seq[-1] not in self.children.keys():
			return self
		return self.children[seq[-1]].longestPrefix(seq[:-1])

	def getNode(self, seq):
		'''
		Return the descendant node corresponding to the exact symbol path
		'seq' or None if not found
		'''
		if len(seq) == 0 :
			return self
		if seq[-1] in self.children.keys():
			return self.children[seq[-1]].getNode(seq[:-1])
		return None

	def increment(self, symbol, context):
		'''
		Add 'symbol' to symbols counter and call increment()
		on node in the subtree whose path is given by 'context'.
		'''
		self.counts[symbol] += 1
		if len(context) > 0:
			child = None
			if context[-1] not in self.children.keys() :
				## First we encounter self.getSymbolPath() + context[-1]
				## during the training
				child = SuffixNode(context[-1], self, self.depth + 1)
				self.children[context[-1]] = child
			else :
				child = self.children[context[-1]]
			## recursive call
			child.increment(symbol, context[:-1])

	def __getitem__(self, key):
		'''
		Return the counts for symbol 'key'
		i.e. the number of times the sequence
		self.getSymbolPath() + key was seen during training
		'''
		if key not in self.counts.keys():
			return 0
		return self.counts[key]

	def getSymbolPath(self):
		'''
		Return the sequence of symbols leading to the node 'self'
		'''
		res = []
		node = self
		while node.parent is not None:
			res.append(node.symbol)
			node = node.parent
		return res

	def totalCount(self, excluded = []):
		'''
		Return the sum of self.count excluding the symbols in
		'excluded' i.e. return the number of times
		self.getSymbolPath() was seen during training
		minus the number of  self.getSymbolPath() + (x in 'excluded')
		'''
		res = 0.
		for k,v in self.counts.iteritems():
			if k not in excluded:
				res += v
		return res

	def numberChildren(self):
		'''
		Return the number of children of self
		'''
		return len(self.children)

	def numberNextSymbols(self):
		'''
		Returns the number of symbols that occured after self.symbol
		in training
		'''
		return len(self.counts) + 0.

	def getRoot(self):
		'''
		Returns the root of of self in the tree
		'''
		res = self
		while res.parent is not None:
			res = res.parent
		return res

	def __str__(self):
		'''
		Human Readable format
		'''
		res = ''.join(['  '] * self.depth)
		res += self.symbol + ' : '+str(self.counts) + '\n'
		for k, v in self.children.iteritems() :
			res += str(v)
		return res

	def __hash__(self):
		return hash(''.join(self.getSymbolPath()))

	def __eq__(self, other):
		return self.getSymbolPath() == other.getSymbolPath()
