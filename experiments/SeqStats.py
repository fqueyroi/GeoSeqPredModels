## TODO: write method to output simple statistics on loaded sequences
##       ie number, min/max/mean length, distribution of length etc.

################################################################################
def symbols(sequences):
	symbols = set()
	for i in range(len(sequences)):
		seq = sequences[i]
		for s in seq :
			symbols.add(s)
	return symbols

################################################################################
def numberOfSymbols(sequences):
	return len(symbols(sequences))

################################################################################
def str_probs(probs):
	h_probs = []
	for p in probs:
		h_probs.append(round(p*100.,2))
	return str(h_probs)
