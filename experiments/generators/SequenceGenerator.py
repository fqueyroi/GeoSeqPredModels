# -*- coding: utf-8 -*-
""" Base inferface for Sequence generation
"""
import sys

class SequenceGenerator(object):

	def __init(self):
		pass

	def generate(self, nb_seq, filename, sep = ' '):
		pass

	def write(self, sequences, filename, sep = ' '):
		file = open(filename,'w')
		id_seq = 0
		for seq in sequences :
			str_seq = str(id_seq)
			if len(seq) > 0 :
				if len(seq) > 1 :
					for i in range(len(seq)-1):
						str_seq += sep+str(seq[i])
				str_seq += sep+str(seq[-1])
			str_seq +='\n'
			file.write(str_seq)
			id_seq += 1
		file.close()
