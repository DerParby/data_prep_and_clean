""" Module with functionalities for blocking based on a dictionary of records,
    where a blocking function must return a dictionary with block identifiers
    as keys and values being sets or lists of record identifiers in that block.
"""


# =============================================================================

def no_blocking(rec_dict):
    """A function which does no blocking but simply puts all records from the
     given dictionary into one block.

     Parameters
     ------------
       rec_dict : Dictionary that holds the record identifiers as keys and
                  corresponding list of record values
    Returns
    -------------
      block_dict:
         dictionary with one entry consisting of all records
  """

    print("Run 'no' blocking:")
    print('  Number of records to be blocked: ' + str(len(rec_dict)))
    print('')

    rec_id_list = list(rec_dict.keys())

    block_dict = {'all_rec': rec_id_list}

    return block_dict


# -----------------------------------------------------------------------------

def conjunctive_block(rec_dict, blocking_keys):
    """Build the blocking index data structure (dictionary) to store blocking
    key values (BKV) as keys and the corresponding list of record identifiers. This blocking strategy follows a conjunctive
    blocking scheme so that two records r and s are in the same block if all blocking key values
    bkv_1[r], bkv_2[r], ..., bkv_n[r] of record r are equal to bkv_1[s], bkv_2[s],..., bkv_n[s] of s.

     Examples:
       If the blocking is based on the 'postcode' and the simple_blocking_key function, the blocks are the following:

        block_dict = {'2000': [rec1_id, rec2_id, rec3_id, ...],
                '2600': [rec4_id, rec5_id, ...],
                  ...
               }
       If the blocking is based on 'postcode' and 'gender':

       block_dict = {'2000f': [rec1_id, rec3_id, ...],
                '2000m': [rec2_id, ...],
                '2600f': [rec5_id, ...],
                '2600m': [rec4_id, ...],
                 ...
               }
      Parameters
      -------------
       rec_dict:
          Dictionary that holds the record identifiers as keys
                       and corresponding list of record values
       blocking_keys:
           List of tuples consisting of the blocking key function and the attribute
           where the function is applied

     Returns
     -------
     block_dict:
         dictionary with blocking key values as key and a list of record identifiers
  """

    block_dict = {}  # The dictionary with blocks to be generated and returned

    print('Run blocking:')
    print('  Number of blocking keys: ' + str(len(blocking_keys)))
    print('  Number of records to be blocked: ' + str(len(rec_dict)))
    print('')

    for (rec_id, rec_values) in rec_dict.items():

        rec_bkv = ''  # Initialise the blocking key value for this record

        # Process selected blocking attributes
        #
        for bf, attr in blocking_keys:
            # Apply blocking function bf and concatenate the result to the existing blocking key value
            rec_bkv += bf(rec_values, attr)
        # Insert the blocking key value and record into blocking dictionary
        #
        if rec_bkv in block_dict:  # Block key value in block index
            # Only need to add the record
            #
            rec_id_list = block_dict[rec_bkv]
            rec_id_list.append(rec_id)

        else:  # Block key value not in block index

            # Create a new block and add the record identifier
            #
            rec_id_list = [rec_id]

        block_dict[rec_bkv] = rec_id_list  # Store the new block

    return block_dict


def disjunctive_block(rec_dict, blocking_keys):
    """Build the blocking index data structure (dictionary) to store blocking
       key values (BKV) as keys and the corresponding list of record identifiers. This blocking strategy follows a disjunctive
       blocking scheme so that two records r and s are in the same block if at least one blocking key-value pair
       bkv_1[r], bkv_2[r], bkv_n[r] of r is equal to bkv_1[s], bkv_2[s], bkv_n[s] of s.


     This method returns a dictionary with blocking key values as its keys and
     list of record identifiers as its values (one list for each block).

     Examples:
       If the blocking is based on the 'postcode' and the simple_blocking_key function, the blocks are the following:
         block_dict = {'2000': [rec1_id, rec2_id, rec3_id, ...],
                       '2600': [rec4_id, rec5_id, ...],
                         ...
                      }
       If the blocking is based on 'postcode' and 'gender':
         block_dict = {'2000': [rec1_id, rec3_id, ...],
                       '2600': [rec2_id, ...],
                       'f': [rec5_id, ...],
                       'm': [rec4_id, ...],
                        ...
                      }

     Parameters
     -----------
       rec_dict      :
           Dictionary that holds the record identifiers as keys
                       and corresponding list of record values
       blocking_keys :
          List of tuples consisting of the blocking key function and the attribute
          where the function is applied

     Returns
     -------
     block_dict:
         dictionary with blocking key values as key and a list of record identifiers
  """

    block_dict = {}  # The dictionary with blocks to be generated and returned

    print('Run blocking:')
    print('  Number of blocking keys: ' + str(len(blocking_keys)))
    print('  Number of records to be blocked: ' + str(len(rec_dict)))
    print('')

    for (rec_id, rec_values) in rec_dict.items():

        # Initialise the blocking key value for this record

        # Process selected blocking blocking keys
        #
        for bf, attr in blocking_keys:
            # Add the attribute index to the blocking key values
            # to distinguish them if they are the same for different attributes
            rec_bkv = str(attr) + bf(rec_values, attr)
            # Insert the blocking key value and record into blocking dictionary
            if rec_bkv in block_dict:  # Block key value in block index
                # Only need to add the record
                rec_id_list = block_dict[rec_bkv]
                rec_id_list.append(rec_id)

            else:  # Block key value not in block index
                # Create a new block and add the record identifier
                rec_id_list = [rec_id]

            block_dict[rec_bkv] = rec_id_list  # Store the new block

    return block_dict


def print_block_statistics(blockA_dict, blockB_dict):
    """Calculate and print some basic statistics about the generated blocks
    """
    print('Statistics of the generated blocks:')

    numA_blocks = len(blockA_dict)
    numB_blocks = len(blockB_dict)

    block_sizeA_list = []
    for rec_id_list in blockA_dict.values():  # Loop over all blocks
        block_sizeA_list.append(len(rec_id_list))

    block_sizeB_list = []
    for rec_id_list in blockB_dict.values():  # Loop over all blocks
        block_sizeB_list.append(len(rec_id_list))

    print('Dataset A number of blocks generated: %d' % (numA_blocks))
    print('    Minimum block size: %d' % (min(block_sizeA_list)))
    print('    Average block size: %.4f' % \
          (float(sum(block_sizeA_list)) / len(block_sizeA_list)))
    print('    Maximum block size: %d' % (max(block_sizeA_list)))
    print('')

    print('Dataset B number of blocks generated: %d' % (numB_blocks))
    print('    Minimum block size: %d' % (min(block_sizeB_list)))
    print('    Average block size: %.4f' % \
          (float(sum(block_sizeB_list)) / len(block_sizeB_list)))
    print('    Maximum block size: %d' % (max(block_sizeB_list)))
    print('')

# End of program.
