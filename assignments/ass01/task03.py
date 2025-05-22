# =============================================================================
# Import necessary modules (Python standard modules first, then other modules)

import sys 

sys.path.append("./")

import time
from statistics import mean

from classification.machine_learning import util
from data import loadDataset
from blocking import blocking_functions
from blocking import blocking, blocking_key_selection
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

attr_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# The list of blocking keys
#
blocking_phonetic_funct_list = [(blocking_functions.phonetic_blocking_key, i) for i in attr_list]
blocking_simple_funct_list = [(blocking_functions.simple_blocking_key, i) for i in attr_list]

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
                                    attr_list, headerA_line)
recB_dict = loadDataset.load_data_set(datasetB_name, rec_idB_col, \
                                    attr_list, headerB_line)

true_match_set = loadDataset.load_truth_data(truthfile_name)


start_time = time.time()

rec = blocking_key_selection.select_blocking_keys(rec_dict_a=recA_dict, 
                                                  rec_dict_b=recB_dict, 
                                                  blocking_key_candidates=blocking_phonetic_funct_list, 
                                                  ground_truth_pairs=true_match_set, 
                                                  training_size=200,
                                                  eps=0.1,
                                                  max_block_size_ratio=0.5)

print(rec)