''''
Data sets DB1BCoupon found at
https://www.transtats.bts.gov/

Database Name: Airline Origin and Destination Survey (DB1B)
Geography:All
Year: 2011
Filter Period: Q1

Needed field: "ITIN_ID","SEQ_NUM","COUPONS","ORIGIN_AIRPORT_ID",
			  "ORIGIN_CITY_MARKET_ID","ORIGIN","ORIGIN_STATE_ABR",
			  "DEST_AIRPORT_ID","DEST_CITY_MARKET_ID","DEST","DEST_STATE_ABR"
'''

import os,sys
import csv

## Downloaded file should be put in the same folder
q1_file = sys.path[0]+'/2011Q1_T_DB1B_COUPON.csv'
sequences = dict({}) ## id itinerary to ORIGIN_AIRPORT_ID/ DEST_AIRPORT_ID sequences
airports = dict({}) ##  ORIGIN_AIRPORT_ID/ DEST_AIRPORT_ID to ORIGIN/DEST (code)
 					##  and ORIGIN_STATE_ABRV/DRIGIN_STATE_ABRV (state)

with open(q1_file,'r') as csv_file:
	csv_reader = csv.DictReader(csv_file, delimiter = ',')
	line_count = 0
	current_seq = []
	current_id_seq = ''
	for row in csv_reader:
		## Coupons infos
		id_seq = row['ITIN_ID']
		seq_len = int(row['COUPONS'])
		if seq_len > 1:
			## Only include trips with more than one flight
			seq_i   = int(row['SEQ_NUM'])
			origin_id = row['ORIGIN_AIRPORT_ID']
			dest_id   = row['DEST_AIRPORT_ID']
			if id_seq != current_id_seq :
				if len(current_seq) > 0:
					sequences[current_id_seq] = current_seq
				current_id_seq = id_seq
				current_seq = ['' for i in range(seq_len + 1)]
			if current_seq[seq_i - 1] != '' and current_seq[seq_i - 1] != origin_id:
				print('Error: seq '+id_seq)
			if current_seq[seq_i] != '' and current_seq[seq_i] != dest_id:
				print('Error: seq '+id_seq)
			current_seq[seq_i - 1] = origin_id
			current_seq[seq_i]     = dest_id

			## Airports infos
			airports[origin_id] = row['ORIGIN'],row['ORIGIN_STATE_ABR']
			airports[dest_id] = row['DEST'],row['DEST_STATE_ABR']

		# line_count += 1
		# if line_count > 5:
		# 	break;

print "Nb Seq = "+str(len(sequences))
print "Nb Airports = "+str(len(airports))

## Write sequences
path_seq_file = sys.path[0]+'/2011Q1_SEQ.csv'
with open(path_seq_file, 'w') as seq_file:
	csv_writer = csv.writer(seq_file, delimiter=',')#, quoting = csv.QUOTE_NONNUMERIC)
	for s_id, seq in sequences.iteritems():
		seq_row = [s_id]
		seq_row.extend(seq)
		csv_writer.writerow(seq_row)

path_airport_file = sys.path[0]+'/2011Q1_AIRPORTS.csv'
with open(path_airport_file, 'w') as airport_file:
	csv_writer = csv.writer(airport_file, delimiter=',')#, quoting = csv.QUOTE_NONNUMERIC)
	for a_id, a_info in airports.iteritems():
		a_row = [a_id,a_info[0],a_info[1]]
		csv_writer.writerow(a_row)
