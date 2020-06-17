'''
Find the best parameters gamma for the GeoFixOrderModel
'''
import sys, os
sys.path.append(''.join([os.path.dirname(__file__), '/..', '/models/']))

import GeoFixOrderModel
import EvalFunctions

def findBestSpread(alphabet, locations, training, testing,
				   eval_fun = EvalFunctions.averageProbNextSymbol,
				   dist_fun = GeoFixOrderModel.Dists[GeoFixOrderModel.DistCalc.EUCLIDIAN],
				   nb_recur = 5, max_gamma = 1.):
	'''
	Use decimal search to find the best gamma value for the GeoFixOrderModel
	according to the evaluation function 'dist_fun'.
	Return:
	-------
		best_gamma, max_score: float, float
	'''
	##TODO: improve search procedure
	max_d = GeoFixOrderModel.getMaxDistance(locations, dist_fun)
	max_score  = 0.
	best_gamma = max_gamma
	for n in range(nb_recur):
		cur_gamma = best_gamma
		next_gammas = [cur_gamma + (i+1)/(10. ** (n+1)) for i in range(9)]
		next_gammas.extend([cur_gamma - (i+1)/(10. ** (n+1)) for i in range(9)])
		for gamma in next_gammas:
			sum_d = GeoFixOrderModel.sumDensities(alphabet, locations, gamma, max_d, dist_fun)
			model = GeoFixOrderModel.GeoFixOrderModel(1, alphabet, locations, gamma,
				dist_fun, max_d, sum_d, False)
			for seq in training:
				model.learn(seq)
			score = eval_fun(model, testing)
			# print '	g = '+str(gamma)+' ss = '+str(round(score*100,4))
			if score > max_score:
				cur_gamma = gamma
				max_score = score
		# print 'cur_g = '+str(cur_gamma)+' best_s = '+str(round(max_score*100,4))
		if cur_gamma == best_gamma:
			break
		best_gamma = cur_gamma
	return best_gamma, max_score

# import FixOrderModel
# import DataModUtils
# import SeqStats
#
# sys.path.append(''.join([os.path.dirname(__file__), '/..', '/data/generators/']))
# import LocationBasedGenerator
#
# print 'gamma,n,score_fix,gamma_geo,score_geo'
# for i in range(1):
# 	gamma = 2./ (10. ** (i+1))
# 	for j in range(1):
# 		for k in range(1):
# 			n = 100*(j+1)
# 			## Generate datasets
# 			gen = LocationBasedGenerator.LocationBasedGenerator(alphabet_size = n, stop_prob = 0.1,gamma = gamma)
# 			locations = gen.locations
# 			sequences =  gen.generate(1000)
# 			sequences = DataModUtils.removeRepetitions(sequences)
#
# 			### Get the unique list of symbols found in sequences
# 			alphabet = SeqStats.symbols(sequences)
# 			# print "Nb Symbols : "+str(len(alphabet))
#
# 			training, testing = DataModUtils.sampleSequences(sequences, ratio_testing = 0.1)
#
# 			## Train models
# 			fix = FixOrderModel.FixOrderModel(1, alphabet)
# 			for seq in training:
# 				fix.learn(seq)
# 			score_fix = EvalFunctions.averageProbNextSymbol(fix, testing)
#
# 			b_gamma, b_score = findBestSpread(alphabet, locations, training, testing)
#
# 			print str(gamma)+','+str(n)+','+str(round(score_fix*100,2))+','+str(b_gamma)+','+str(round(b_score*100,2))
