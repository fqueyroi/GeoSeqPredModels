# -*- coding: utf-8 -*-
"""HON Suffix Tree

Special Suffix Tree used for the HON Model
"""

import SuffixTree

class HONSuffixNode(SuffixTree.SuffixNode):

	def __init__(self, symbol, parent, depth = 0, is_rule = False):
		super(HONSuffixNode, self).__init__(symbol, parent, depth)
		self.is_rule = is_rule

	def numberOfRules(self):
		res = 0
		if self.is_rule:
			res = 1
		for k,v in self.children.iteritems():
			res += v.numberOfRules()
		return res

	def longestPrefix(self, seq):
		res = self
		current = self
		cseq = seq
		while  len(cseq) > 0 and cseq[-1] in current.children.keys():
			current =  current.children[cseq[-1]]
			if current.is_rule:
				res = current
			cseq = cseq[:-1]
		return res

	def increment(self, symbol, context):
		self.counts[symbol] += 1
		if len(context) > 0:
			child = None
			if context[-1] not in self.children.keys() :
				child = HONSuffixNode(context[-1], self, self.depth + 1)
				self.children[context[-1]] = child
			else :
				child = self.children[context[-1]]
			child.increment(symbol, context[:-1])

	def __str__(self):
		res = ''.join(['  '] * self.depth)
		res += self.symbol + ' : '+str(self.counts)
		if self.is_rule:
			res += " RULE"
		res += '\n'
		for k, v in self.children.iteritems() :
			res += str(v)
		return res
