# -*- coding: utf-8 -*-
'''
Contains function to read/write files
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
def readLocations(filename, col_id, col_x, col_y, sep = ',', header = True):
	locations = dict()
	file = open(filename,'r')
	count_line = 0
	for line in file :
		if header :
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
def writeSequences(self, sequences, filename, sep = ' '):
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
