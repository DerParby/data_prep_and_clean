""" Module with functionalities for classifying a dictionary of record pairs
    and their similarities based on a similarity threshold.

    Each function in this module returns two sets, one with record pairs
    classified as matches and the other with record pairs classified as
    non-matches.
"""


# =============================================================================
import math
from typing import Tuple, List


def exact_classify(sim_vec_dict: dict[(str, str):list]) -> Tuple[set, set]:
    """
    Method to classify the given similarity vector dictionary assuming only
    exact matches (having all similarities of 1.0) are matches.

    The classification is based on the exact matching of attribute values,
    that is the similarity vector for a given record pair must contain 1.0
    for all attribute values.

    Example:
       (recA1, recB1) = [1.0, 1.0, 1.0, 1.0] => match
       (recA2, recB5) = [0.0, 1.0, 0.0, 1.0] = non-match

    Parameters
    ----------
    sim_vec_dict:
        dictionary of record pairs with lists of similarities as value

    Returns
    -------
    class_match_set,class_nonmatch_set:
        (set of matches, set of non-matches)
  """

    print('Exact classification of %d record pairs' % (len(sim_vec_dict)))

    class_match_set = set()
    class_nonmatch_set = set()

    # Iterate over all record pairs
    #
    for (rec_id_tuple, sim_vec) in sim_vec_dict.items():

        sim_sum = sum(sim_vec)  # Sum all attribute similarities

        if sim_sum == len(sim_vec):  # All similarities were 1.0
            class_match_set.add(rec_id_tuple)
        else:
            class_nonmatch_set.add(rec_id_tuple)

    print('  Classified %d record pairs as matches and %d as non-matches' % \
          (len(class_match_set), len(class_nonmatch_set)))
    print('')

    return class_match_set, class_nonmatch_set


# -----------------------------------------------------------------------------
# TODO Implement the threshold classification
def threshold_classify(sim_vec_dict: dict[(str, str):list], sim_thres: float) -> Tuple[set, set]:
    """
    Method to classify the given record pairs in the similarity vector dictionary using a given similarity threshold
    (in the range of 0.0 to 1.0). A record pair is classified as a match if the average similarity is above
    or equal to the given threshold, otherwise it is classified as a non-match.

    Parameters
    -----------
        sim_vec_dict :
            Dictionary of record pairs with the identifiers as key and a list of similarities representing the similarity vector
        sim_thres    :
            similarity threshold.

    Returns
    ---------
     class_match_set,class_nonmatch_set:
        (set of matches, set of non-matches)
  """

    assert sim_thres >= 0.0 and sim_thres <= 1.0, sim_thres

    print('Similarity threshold based classification of %d record pairs' % \
          (len(sim_vec_dict)))
    print('  Classification similarity threshold: %.3f' % (sim_thres))

    class_match_set = set()
    class_nonmatch_set = set()

    # Iterate over all record pairs
    #
    for (rec_id_tuple, sim_vec) in sim_vec_dict.items():
        pass
        # ************ ADD YOUR code ****************************
        # ************ End of your code *******************************************

    print('  Classified %d record pairs as matches and %d as non-matches' % \
          (len(class_match_set), len(class_nonmatch_set)))
    print('')

    return class_match_set, class_nonmatch_set


# -----------------------------------------------------------------------------

# TODO Implement the minimum threshold classification
def min_threshold_classify(sim_vec_dict, sim_thres) -> Tuple[set, set]:
    """
    Method to classify the given record pairs in the similarity vector dictionary using a given similarity threshold
    (in the range of 0.0 to 1.0). A record pair is classified as a match if all similarities are above or equal to
    the given threshold, otherwise it is classified as a non-match.

    Parameters
    -----------
        sim_vec_dict :
            Dictionary of record pairs with the identifiers as key and a list of similarities representing the similarity vector
        sim_thres    :
            similarity threshold.

    Returns
    --------
        class_match_set,class_nonmatch_set:
            (set of matches, set of non-matches)
  """

    assert sim_thres >= 0.0 and sim_thres <= 1.0, sim_thres

    print('Minimum similarity threshold based classification of ' + \
          '%d record pairs' % (len(sim_vec_dict)))
    print('Classification similarity threshold: %.3f' % sim_thres)

    class_match_set = set()
    class_nonmatch_set = set()

    # Iterate over all record pairs
    #
    for (rec_id_tuple, sim_vec) in sim_vec_dict.items():
        pass
        # ADD your code

    print('  Classified %d record pairs as matches and %d as non-matches' % \
          (len(class_match_set), len(class_nonmatch_set)))
    print('')

    return class_match_set, class_nonmatch_set


# -----------------------------------------------------------------------------

# TODO Implement the weighted threshold classification based on a weight vector
def weighted_similarity_classify(sim_vec_dict, weight_vec, sim_thres) -> Tuple[set, set]:
    """
    Method to classify the given record pairs in the similarity vector dictionary using a given similarity
    threshold and weight vector (in the range of 0.0 to 1.0). The similarities are aggregated using the weight vector.
    A record pair is classified as a match if the aggregated similarity is above or equal to the given threshold,
    otherwise it is classified as a non-match.

    Parameters
    -----------
        sim_vec_dict :
            Dictionary of record pairs with the identifiers as key and a list of similarities representing the similarity vector
        weight_vec :
            weight vector
        sim_thres    :
            similarity threshold.

    Returns
    --------
     class_match_set,class_nonmatch_set:
            (set of matches, set of non-matches)

"""

    assert 0.0 <= sim_thres <= 1.0, sim_thres

    # Check weights are available for all attributes
    #
    first_sim_vec = list(sim_vec_dict.values())[0]
    assert len(weight_vec) == len(first_sim_vec), len(weight_vec)

    print('Weighted similarity based classification of %d record pairs' % \
          (len(sim_vec_dict)))
    print('  Weight vector: %s' % (str(weight_vec)))
    print('  Classification similarity threshold: %.3f' % sim_thres)

    class_match_set = set()
    class_nonmatch_set = set()

    # Iterate over all record pairs
    #
    for (rec_id_tuple, sim_vec) in sim_vec_dict.items():
        # ******* Implement weighted similarity classification ********************
        pass
        # ************ End of your code *******************************************

    print('Classified %d record pairs as matches and %d as non-matches' % \
          (len(class_match_set), len(class_nonmatch_set)))
    print('')

    return class_match_set, class_nonmatch_set


# TODO Implement an automatic method for computing the weight vector
def automatic_weight_computation(rec_dict_a: dict, rec_dict_b: dict, compared_attribute_idx) -> List[float]:
    """
    Method to compute the weights for a list of attributes using the number of unique values of an attribute.

    Parameters
    ------------
        rec_dict_a:
            dictionary of records from data source A
        rec_dict_b:
            dictionary of records from data source B
        compared_attribute_idx:
            list of attribute pairs used for comparison

    Returns
    --------
    list of weights as floats
    """
    weight_vector = None
    return weight_vector
