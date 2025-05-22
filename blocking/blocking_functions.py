""" Module to define blocking functions. Each function computes for a record and a specified attribute a
blocking key value that can be concatenated with other blocking key values
"""


def simple_blocking_key(rec_values, attr):
    """Builds the blocking index data structure (dictionary) to store blocking
     key values (BKV) as keys and the corresponding list of record identifiers.

     A blocking is implemented that concatenates Soundex encoded values of
     attribute values.

     Parameters
     -------------
       rec_values:
         list of record values
       attr :
         attribute index

     This method returns a blocking key value for a certain attribute value of a record
  """
    return rec_values[attr]


# TODO Implement Soundex based blocking
def phonetic_blocking_key(rec_values, attr):
    """
     A blocking key is generated using Soundex
     Parameter Description:
       rec_values      : list of record values
       attr : attribute index

     This method returns a blocking key value for a certain attribute value of a record
  """
    rec_bkv = ''
    return rec_bkv


# TODO Implement SLK based blocking
def slk_blocking_key(rec_values, attribute_index_list):
    """

     A blocking key is generated using statistical linkage key (SLK-581)
     blocking approach as used in real-world linkage applications:

     http://www.aihw.gov.au/WorkArea/DownloadAsset.aspx?id=60129551915

     A SLK-581 blocking key is the based on the concatenation of:
     - 3 letters of family name
     - 2 letters of given name
     - Date of birth
     - Sex

     Parameter Description:
       rec_dict          : Dictionary that holds the record identifiers as
                           keys and corresponding list of record values
       attribute_index_list    : List of attribute indices where each attribute is required for generating SLK-581

     This method returns a blocking key value utilizing SLK-581
  """
    # *********** Implement SLK-581 function here ***********
    slk = ''
    return slk
