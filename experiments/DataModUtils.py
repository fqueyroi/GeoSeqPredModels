# -*- coding: utf-8 -*-
'''
Contains function to read/write files
and create sample/testing datasets.
'''

import sys
import random

######################################################################################
def readFile(filename,is_line_id = True, sep = ' ') :
	sequences = []
	file = open(filename,'r')
	count_line = 0
	for line in file :
		if len(line) > 0 :
			count_line += 1
			split_line = []
			if sep == '':
				split_line = list(line.strip())
			else :
				split_line = line.strip().split(sep)

			seq = []
			if is_line_id :
				id_seq = split_line[0]
				seq = split_line[1:]
				sequences.append(seq)
			else :
				sequences.append(split_line)
	file.close()
	return sequences

######################################################################################
def readText(filename) :
	sequence = []
	file = open(filename,'r')
	count_line = 0
	for line in file :
		count_line += 1
		split_line = list(line.strip())
		for e in split_line:
			sequence.append(e)
		sequence.append(' ')
	file.close()
	return sequence

######################################################################################
def readTextByLines(filename) :
	sequences = []
	file = open(filename,'r')
	count_line = 0
	for line in file :
		count_line += 1
		split_line = list(line.strip())
		sequences.append(split_line)
	file.close()
	return sequences

######################################################################################
def cutText(text, ratio_training):
	training = []
	testing  = []
	end_training = int(round(len(text)*ratio_training))
	for i in range(end_training):
		training.append(text[i])
	for i in range(end_training,len(text)):
		testing.append(text[i])
	return training, testing

######################################################################################
def cutEachSequences(sequences,len_test) :
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

######################################################################################
def sampleAndCutSequences(sequences, len_test, ratio_testing) :
	size_test = int(round(len(sequences)*ratio_testing))
	build_seqs = []
	test_contexts = []
	test_seqs  = []

	for i in range(len(sequences)) :
		seq = sequences[i]
		if random.random() >= ratio_testing:
			build_seqs.append(seq)
		else :

			if len(seq) <= len_test :
				test_contexts.append([seq[0]])
				test_seqs.append(seq[1:])
				# test_contexts.append(seq[:2])
				# test_seqs.append(seq[2])
			else :
				test_contexts.append(seq[:-len_test])
				test_seqs.append(seq[-len_test:])
				# test_contexts.append(seq[:2])
				# test_seqs.append(seq[2:])
 	return build_seqs, test_contexts, test_seqs

######################################################################################
def sampleSequences(sequences, ratio_testing):
	build_seqs = []
	test_seqs  = []
	for i in range(len(sequences)):
		if random.random() < ratio_testing:
			test_seqs.append(sequences[i])
		else:
			build_seqs.append(sequences[i])
	return build_seqs, test_seqs

######################################################################################
def removeRepetitions(sequences):
	nsequences = []
	for seq in sequences:
		nseq = []
		for s in seq:
			if len(nseq) == 0 or s != nseq[-1]:
				nseq.append(s)
		nsequences.append(nseq)
	return nsequences

######################################################################################
def str_probs(probs):
	h_probs = []
	for p in probs:
		h_probs.append(round(p*100.,2))
	return str(h_probs)

######################################################################################
def symbols(sequences):
	symbols = set()
	for i in range(len(sequences)):
		seq = sequences[i]
		for s in seq :
			symbols.add(s)
	return symbols


######################################################################################
def numberOfSymbols(sequences):
	return len(symbols(sequences))


######################################################################################
def readLocations(filename, col_id, col_x, col_y, sep = ','):
	locations = dict()
	file = open(filename,'r')
	count_line = 0
	for line in file :
		if count_line == 0:
			count_line += 1
			continue
		if len(line) == 0:
			count_line += 1
			continue
		count_line += 1
		split_line = line.strip().split(sep)
		# print split_line[col_id]+" "+split_line[col_x]+" "+split_line[col_y]
		if split_line[col_x] == "" or split_line[col_y] == "":
			continue
		id = split_line[col_id]
		x = float(split_line[col_x])
		y = float(split_line[col_y])
		locations[id] = (x,y)

	file.close()
	return locations
