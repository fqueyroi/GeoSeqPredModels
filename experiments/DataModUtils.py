# -*- coding: utf-8 -*-
'''
Contains functions to prepare
datasets for learning/testing
'''

import sys
import random

################################################################################
def cutEndOfSequences(sequences,len_test) :
	build_seqs = []
	test_seqs  = []
	if len_test == 0:
		return sequences, []

	for seq in sequences :
		if len(seq) < len_test :
			build_seqs.append([])
			test_seqs.append(seq)
		else :
			build_seqs.append(seq[:-len_test])
			test_seqs.append(seq[-len_test:])
 	return build_seqs, test_seqs

################################################################################
def sampleSequences(sequences, ratio_testing):
	build_seqs = []
	test_seqs  = []
	for i in range(len(sequences)):
		if random.random() < ratio_testing:
			test_seqs.append(sequences[i])
		else:
			build_seqs.append(sequences[i])
	return build_seqs, test_seqs

################################################################################
def removeRepetitions(sequences):
	nsequences = []
	for seq in sequences:
		nseq = []
		for s in seq:
			if len(nseq) == 0 or s != nseq[-1]:
				nseq.append(s)
		nsequences.append(nseq)
	return nsequences
################################################################################

def filterAlphabet(alphabet, categories):
	filtered_alp = []
	for i in alphabet:
		if i in categories:
			filtered_alp.append(i)
	return filtered_alp
################################################################################

def filterSequences(sequences, categories):
	filtered_seq = []
	valid=True
	for i in range(len(sequences)):
		for j in range(len(sequences[i])):
			if sequences[i][j] not in categories:
				valid =False
		if valid == True:
			filtered_seq.append(sequences[i])
	return filtered_seq
