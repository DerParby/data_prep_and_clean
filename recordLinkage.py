# ============================================================================
# Record linkage software for the Data Wrangling course, 2021.
# Version 1.0
#
# =============================================================================

"""Main module for linking records from two files.

   This module calls the necessary modules to perform the functionalities of
   the record linkage process.
"""

# =============================================================================
# Import necessary modules (Python standard modules first, then other modules)

import time
from statistics import mean

from classification.machine_learning import util
from data import loadDataset
from blocking import blocking_functions
from blocking import blocking
from comparison import comparison
from comparison import string_functions
from classification import threshold_classification
from evaluation import evaluation as evaluation

# =============================================================================

# ******** Uncomment to select a pair of datasets **************

datasetA_name = 'datasets/clean-A-1000.csv'
datasetB_name = 'datasets/clean-B-1000.csv'
truthfile_name = 'datasets/clean-true-matches-1000.csv'

# datasetA_name = 'datasets/clean-A-10000.csv'
# datasetB_name = 'datasets/clean-B-10000.csv'
# truthfile_name = 'datasets/clean-true-matches-10000.csv'

# datasetA_name = 'datasets/little-dirty-A-1000.csv'
# datasetB_name = 'datasets/little-dirty-B-1000.csv'
# truthfile_name = 'datasets/little-dirty-true-matches-1000.csv'

# datasetA_name = 'datasets/little-dirty-A-10000.csv'
# datasetB_name = 'datasets/little-dirty-B-10000.csv'
# truthfile_name = 'datasets/little-dirty-true-matches-10000.csv'


headerA_line = True  # Dataset A header line available - True or Flase
headerB_line = True  # Dataset B header line available - True or Flase

# The two attribute numbers that contain the record identifiers
#
rec_idA_col = 0
rec_idB_col = 0

# The list of attributes to be used either for blocking or linking
#
# For the example data sets:
#  0: rec_id
#  1: first_name
#  2: middle_name
#  3: last_name
#  4: gender
#  5: current_age
#  6: birth_date
#  7: street_address
#  8: suburb
#  9: postcode
# 10: state
# 11: phone
# 12: email

attrA_list = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11]
attrB_list = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11]

# The list of blocking keys
#
blocking_funct_listA = [(blocking_functions.simple_blocking_key, 4), (blocking_functions.simple_blocking_key, 3)]
blocking_funct_listB = [(blocking_functions.simple_blocking_key, 4), (blocking_functions.simple_blocking_key, 3)]

# The list of comparison tuples (comparison function, attribute number in record A,
# attribute number in record B)
#
exact_comp_funct_list = [(string_functions.exact_comp, 1, 1),  # First name
                         (string_functions.exact_comp, 4, 4),  # Middle name
                         (string_functions.exact_comp, 3, 3),  # Last name
                         (string_functions.exact_comp, 8, 8),  # Suburb
                         (string_functions.exact_comp, 10, 10),  # State
                         ]
approx_comp_funct_list = [(string_functions.jaro_comp, 1, 1),  # First name
                          (string_functions.jaro_comp, 2, 2),  # Middle name
                          (string_functions.jaro_comp, 3, 3),  # Last name
                          ]

# =============================================================================
#
# Step 1: Load the two datasets from CSV files

start_time = time.time()

recA_dict = loadDataset.load_data_set(datasetA_name, rec_idA_col, \
                                      attrA_list, headerA_line)
recB_dict = loadDataset.load_data_set(datasetB_name, rec_idB_col, \
                                      attrB_list, headerB_line)

# Load data set of true matching pairs
#
true_match_set = loadDataset.load_truth_data(truthfile_name)
weight_vector = [2.0, 1.0, 2.0, 2.0, 2.0, 1.0, 1.0]
loading_time = time.time() - start_time

# -----------------------------------------------------------------------------
# Step 2: Block the datasets

start_time = time.time()

# Select one blocking technique

# No blocking (all records in one block)
#
# blockA_dict = blocking.noBlocking(recA_dict)
# blockB_dict = blocking.noBlocking(recB_dict)


blockA_dict = blocking.conjunctive_block(recA_dict, blocking_funct_listA)
blockB_dict = blocking.conjunctive_block(recB_dict, blocking_funct_listB)

blocking_time = time.time() - start_time

# Print blocking statistics
#
blocking.print_block_statistics(blockA_dict, blockB_dict)

# -----------------------------------------------------------------------------
# Step 3: Compare the candidate pairs

start_time = time.time()
sim_vec_dict = comparison.compare_blocks(blockA_dict, blockB_dict, \
                                        recA_dict, recB_dict, \
                                        approx_comp_funct_list)

comparison_time = time.time() - start_time

# -----------------------------------------------------------------------------
# Step 4: Classify the candidate pairs using k-fold cross validation

start_time = time.time()
# list of quality measures to compute the average
accuracy = []
precision = []
recall = []
fmeasure = []
# k_fold cross validation for ML classification but also applicable for threshold-based classification
k_fold_list = util.kfold_split(sim_vec_dict, true_match_set, 5)
for train_dict, test_dict, test_true_matches_fold, all_comparisons in k_fold_list:
    # Exact matching based classification
    # exact classification
    class_match_set, class_nonmatch_set = \
        threshold_classification.exact_classify(sim_vec_dict)
    # Step 5.2: Evaluate the quality of the classification within cross validation
    linkage_result = evaluation.confusion_matrix(class_match_set,
                                                 class_nonmatch_set,
                                                 test_true_matches_fold,
                                                 all_comparisons)
    accuracy.append(evaluation.accuracy(linkage_result))
    precision.append(evaluation.precision(linkage_result))
    recall.append(evaluation.recall(linkage_result))
    fmeasure.append(evaluation.fmeasure(linkage_result))
classification_time = time.time() - start_time

# -----------------------------------------------------------------------------
# Step 5.1: Evaluate the blocking

# Get the number of record pairs compared
#
num_comparisons = len(sim_vec_dict)

# Get the number of total record pairs to compared if no blocking used
#
all_comparisons = len(recA_dict) * len(recB_dict)

# Get the list of identifiers of the compared record pairs
#
cand_rec_id_pair_list = sim_vec_dict.keys()

# Blocking evaluation
#
rr = evaluation.reduction_ratio(num_comparisons, all_comparisons)
pc = evaluation.pairs_completeness(cand_rec_id_pair_list, true_match_set)
pq = evaluation.pairs_quality(cand_rec_id_pair_list, true_match_set)

print('Blocking evaluation:')
print('  Reduction ratio:    %.3f' % rr)
print('  Pairs completeness: %.3f' % pc)
print('  Pairs quality:      %.3f' % pq)
print('')

# Linkage evaluation
#


accuracy = mean(accuracy)
precision = mean(precision)
recall = mean(recall)
fmeasure = mean(fmeasure)

print('Linkage evaluation:')
print('  Accuracy:    %.3f' % accuracy)
print('  Precision:   %.3f' % precision)
print('  Recall:      %.3f' % recall)
print('  F-measure:   %.3f' % fmeasure)
print('')

linkage_time = loading_time + blocking_time + comparison_time + \
               classification_time
print('Blocking runtime required for linkage: %.3f sec' % blocking_time)
print('comparison runtime required for linkage: %.3f sec' % comparison_time)
print('classification runtime required for linkage: %.3f sec' % classification_time)
print('Total runtime required for linkage: %.3f sec' % linkage_time)

# -----------------------------------------------------------------------------

# End of program.
