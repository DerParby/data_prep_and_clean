""" Module to define blocking functions. Each function computes for a record and a specified attribute a
blocking key value that can be concatenated with other blocking key values
"""
import re

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


def soundex(name):
    """
    Generate the Soundex code for a given name.
    """
    name = name.upper()
    if not name:
        return "0000"

    # Initialize the Soundex code with the first letter of the name
    soundex_code = name[0]

    # Soundex mappings
    mappings = {
        'BFPV': '1',
        'CGJKQSXZ': '2',
        'DT': '3',
        'L': '4',
        'MN': '5',
        'R': '6'
    }

    def get_code(char):
        """Return the Soundex code for a given character."""
        for key, value in mappings.items():
            if char in key:
                return value
        return ''

    # Encode the rest of the string
    prev_code = get_code(name[0])
    for char in name[1:]:
        current_code = get_code(char)
        if current_code != prev_code and current_code:
            soundex_code += current_code
        prev_code = current_code

    # Pad the Soundex code with zeros and return the first four characters
    return (soundex_code + '000')[:4]



def phonetic_blocking_key(rec_values, attr):
    """
     A blocking key is generated using Soundex
     Parameter Description:
       rec_values      : list of record values
       attr : attribute index

     This method returns a blocking key value for a certain attribute value of a record
  """
    value = rec_values[attr]
    return soundex(value)


def extract_consonants(name, length, padding_char):
    """
    Extract consonants from a name and pad to the specified length.
    """
    consonants = re.sub(r'[^BCDFGHJKLMNPQRSTVWXYZ]', '', name)[:length]
    return consonants.ljust(length, padding_char)


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
    family_name = rec_values[attribute_index_list[0]].upper()
    given_name = rec_values[attribute_index_list[1]].upper()
    dob = re.sub(r'\D', '', rec_values[attribute_index_list[2]])  # Remove non-digit characters
    sex = rec_values[attribute_index_list[3]].upper()

    # Extract consonants from family and given names
    family_consonants = extract_consonants(family_name, 3, '2')
    given_consonants = extract_consonants(given_name, 2, '2')

    # Combine components to form the SLK
    slk = family_consonants + given_consonants + dob + sex
    return slk
