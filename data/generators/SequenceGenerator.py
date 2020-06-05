# -*- coding: utf-8 -*-
"""
Base inferface for Sequence generation
"""
## TODO: create generators that use categorical dataset
##		maybe using a Hidden Markov model where the state are the categories 

class SequenceGenerator(object):

	def __init(self):
		pass

	def generate(self, nb_seq):
		'''
		Returns:
		--------
		sequences: list of list of str
			should be of size nb_seq
		'''
		pass
