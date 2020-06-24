
import sys, os
sys.path.append(''.join([os.path.dirname(__file__), '/..']))
import DataModUtils
import SeqStats
import csv

sys.path.append(''.join([os.path.dirname(__file__), '/../..', '/models/']))
import PPMCModel
import FixOrderModel
import ThereAndBackModel
import HONModel
import EvalFunctions

sys.path.append(''.join([os.path.dirname(__file__), '/../..', '/data/generators/']))
import HierarchicalReturnGenerator

#train each models and return the results
def learning(func_table, base, min_k, max_k, len_test, training, testing, test_contexts):
    result = []
    for k, v in func_table.iteritems():
        result_func= dict.fromkeys(['model','k', 'score_1', 'score_2', 'score_3'])
        result_func.update(base)
        func, args, name = func_table[k]

        for i in range(min_k, max_k + 1):
            model = func(i, *args)
            for seq in training:
                model.learn(seq)

        func1 = EvalFunctions.averageProbNextSymbol(model, testing)
        func2 = EvalFunctions.averageProbAllSymbols(model, testing)
        func3 = EvalFunctions.averageProbNextKSymbols(model, test_contexts, testing, len_test)

        print str(model)
        print "	probs averageProbNextSymbol: " + str(round(func1 * 100., 2))
        print "	probs averageProbAllSymbols: " + str(round(func2 * 100., 2))
        print "	probs averageProbNextKSymbols: " + SeqStats.str_probs(func3)

        result_func.update({'model': name, 'k': len_test, 'score_1': str(round(func1 * 100., 2)), 'score_2': str(round(func2 * 100., 2)), 'score_3': SeqStats.str_probs(func3)})
        result.append(result_func)
    return result



choices = ["Location", "Categories", "CategoriesSymb"]
generator = choices[1]

### PARAMETERS
### (Should list all variables for the experiments)
min_k = 1  ## minimum context length
max_k = 1  ## maximum context length
len_test = [1,2,3]
a_size = [100, 1000, 10000]
stop_prob = 0.1
prob_return_node = 0.1
result = []

for j in a_size:
    for i in len_test:

        base = {
            "alphabet_size": j,
            "stop_prob": stop_prob,
            "prob_return_node": prob_return_node
        }

        ## Generate datasets
        gen = HierarchicalReturnGenerator.HierarchicalReturnGenerator(alphabet_size=j, k=i, stop_prob=stop_prob, prob_return_node=prob_return_node)
        locations = gen.network

        sequences = gen.generate(400)
        sequences = DataModUtils.removeRepetitions(sequences)

        print "Nb Seqs : " + str(len(sequences))

        ### Get the unique list of symbols found in sequences
        alphabet = SeqStats.symbols(sequences)
        print "Nb Symbols : " + str(len(alphabet))

        ### Create Training/Testing subsets
        training, test_contexts, testing = [], [], []
        training, testing = DataModUtils.cutEndOfSequences(sequences, i)
        test_contexts = training

        func_table = {
            1: (PPMCModel.PPMCModel, [alphabet], "PPMC"),
            2: (ThereAndBackModel.ThereAndBackModel, [alphabet], "There And Back"),
            3: (HONModel.HONModel, [alphabet], "HON"),
            4: (FixOrderModel.FixOrderModel, [alphabet], "Fix Order"),
        }
        result.append(learning(func_table, base,min_k, max_k, i, training, testing, test_contexts))

#write result in a file
path_seq_file = sys.path[0] + '/RES_Return_Generator.csv'
with open(path_seq_file, 'w') as seq_file:
    csv_writer = csv.DictWriter(seq_file, result[0][0].keys())
    csv_writer.writeheader()
    for i in result:
        for j in i:
            csv_writer.writerow(j)




