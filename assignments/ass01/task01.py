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
import sys 

sys.path.append("./")

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
datasetB_name = 'datasets/little-dirty-A-1000.csv'

headerA_line = True  # Dataset A header line available - True or Flase
headerB_line = True  # Dataset B header line available - True or Flase

# The two attribute numbers that contain the record identifiers
#
rec_idA_col = 0
rec_idB_col = 0

# The list of attributes to be used either for blocking or linking
#
# For the example data sets:
attributes = {
    0: "rec_id",
    1: "first_name",
    2: "middle_name",
    3: "last_name",
    4: "gender",
    5: "current_age",
    6: "birth_date",
    7: "street_address",
    8: "suburb",
    9: "postcode",
    10: "state",
    11: "phone",
    12: "email"
}

attr_list = [1, 2, 3, 8]



#
# Step 1: Load the two datasets from CSV files

start_time = time.time()

recA_dict = loadDataset.load_data_set(datasetA_name, rec_idA_col, \
                                      attr_list, headerA_line)
recB_dict = loadDataset.load_data_set(datasetB_name, rec_idB_col, \
                                      attr_list, headerB_line)

# -----------------------------------------------------------------------------
# Step 2: Block the datasets




for attr in attr_list:
    
    print(f"{attributes[attr]}")
    start_time = time.time()

    blocking_funct_list = [(blocking_functions.simple_blocking_key, attr)]

    blockA_dict = blocking.conjunctive_block(recA_dict, blocking_funct_list)
    blockB_dict = blocking.conjunctive_block(recB_dict, blocking_funct_list)

    blocking_time = time.time() - start_time

    blocking.print_block_statistics(blockA_dict, blockB_dict)

print("\n\n\n--------------------------\n\n\n")

for attr in attr_list:
    
    print(f"{attributes[attr]}")
    start_time = time.time()

    blocking_funct_list = [(blocking_functions.phonetic_blocking_key, attr)]

    blockA_dict = blocking.conjunctive_block(recA_dict, blocking_funct_list)
    blockB_dict = blocking.conjunctive_block(recB_dict, blocking_funct_list)

    blocking_time = time.time() - start_time

    blocking.print_block_statistics(blockA_dict, blockB_dict)