# -*- coding: utf-8 -*-
'''
Contains functions to prepare
datasets for learning/testing
'''

import sys
import random

################################################################################
def splitSequenceRandom(seq, ratio_training):
	training = []
	testing  = []
	end_training = int(round(len(seq)*ratio_training))
	for i in range(end_training):
		training.append(seq[i])
	for i in range(end_training,len(seq)):
		testing.append(seq[i])
	return training, testing

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
