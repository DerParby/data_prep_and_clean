""" Module with functionalities to evaluate the results of a record linkage
    exercise regarding linkage quality as well as complexity.
"""
from sklearn import metrics


# =============================================================================

def confusion_matrix(class_match_set, class_nonmatch_set, true_match_set,
                     all_comparisons):
    """Compute the confusion (error) matrix which has the following form:

     +-----------------+-----------------------+----------------------+
     |                 |  Predicted Matches    | Predicted NonMatches |
     +=================+=======================+======================+
     | True  Matches   | True Positives (TP)   | False Negatives (FN) |
     +-----------------+-----------------------+----------------------+
     | True NonMatches | False Positives (FP)  | True Negatives (TN)  |
     +-----------------+-----------------------+----------------------+

     The four values calculated in the confusion matrix (TP, FP, TN, and FN)
     are then the basis of linkag equality measures such as precision and
     recall.

     Parameter Description:
       class_match_set    : Set of classified matches (record identifier
                            pairs)
       class_nonmatch_set : Set of classified non-matches (record identifier
                            pairs)
       true_match_set     : Set of true matches (record identifier pairs)
       all_comparisons    : The total number of comparisons between all record
                            pairs

     This function returns a list with four values representing TP, FP, FN,
     and TN.
  """

    print('Calculating confusion matrix using %d classified matches, %d ' % \
          (len(class_match_set), len(class_nonmatch_set)) + 'classified ' + \
          'non-matches, and %d true matches' % (len(true_match_set)))

    num_tp = 0  # number of true positives
    num_fp = 0  # number of false positives
    num_tn = 0  # number of true negatives
    num_fn = 0  # number of false negatives

    # Iterate through the classified matches to check if they are true matches or
    # not
    #
    for rec_id_tuple in class_match_set:
        if (rec_id_tuple in true_match_set):
            num_tp += 1
        else:
            num_fp += 1

    # Iterate through the classified non-matches to check of they are true
    # non-matches or not
    #
    for rec_id_tuple in class_nonmatch_set:

        # Check a record tuple is only counted once
        #
        assert rec_id_tuple not in class_match_set, rec_id_tuple
        if rec_id_tuple in true_match_set:
            num_fn += 1
        else:
            num_tn += 1

    # Finally count all missed true matches to the false negatives
    #
    for rec_id_tuple in true_match_set:
        if ((rec_id_tuple not in class_match_set) and \
                (rec_id_tuple not in class_nonmatch_set)):
            num_fn += 1
    num_tn = all_comparisons - num_tp - num_fp - num_fn
    print('  TP=%s, FP=%d, FN=%d, TN=%d' % (num_tp, num_fp, num_fn, num_tn))
    print('')

    return [num_tp, num_fp, num_fn, num_tn]


# =============================================================================
# TODO Implement accuracy
def accuracy(confusion_matrix):
    """Computes accuracy using the given confusion matrix.

     Accuracy is calculated as (TP + TN) / (TP + FP + FN + TN).

     Parameters
     -----------
      confusion_matrix :
         The matrix with TP, FP, FN, TN values.

     Returns
     --------
       accuracy:
          accuracy as float value
  """
    accuracy = 0.0
    # ADD
    return accuracy


# -----------------------------------------------------------------------------
# TODO Implement precision
def precision(confusion_matrix):
    """Computes precision using the given confusion matrix.

     Precision is calculated as TP / (TP + FP).

     Parameters
     -----------
      confusion_matrix :
         The matrix with TP, FP, FN, TN values.

      Returns
     --------
       precision:
          precision as float value
  """

    precision = 0.0
    # ADD
    return precision


# -----------------------------------------------------------------------------
# TODO Implement recall
def recall(confusion_matrix):
    """Compute recall using the given confusion matrix.

     Recall is calculated as TP / (TP + FN).

     Parameters
     -----------
      confusion_matrix :
         The matrix with TP, FP, FN, TN values.

     Returns
     --------
       recall:
          recall as float value
  """

    recall = 0.0
    # ADD
    return recall


# -----------------------------------------------------------------------------
# TODO implement F-measure
def fmeasure(confusion_matrix):
    """Compute the f-measure of the linkage.

     The f-measure is calculated as:

              2 * (precision * recall) / (precision + recall).

     Parameters
     -----------
      confusion_matrix :
         The matrix with TP, FP, FN, TN values.

     Returns
     --------
       recall:
          F-measure as float value
  """
    f_measure = 0.0
    return f_measure


# =============================================================================
# Different linkage complexity measures
# TODO Implement reduction ratio
def reduction_ratio(num_comparisons, all_comparisons):
    """Computes the reduction ratio using the given confusion matrix.

     Reduction ratio is calculated as 1 - num_comparison / (TP + FP + FN+ TN).

     Parameters
     ------------
       num_comparisons :
         The number of candidate record pairs
       all_comparisons :
         The total number of comparisons between all record
                         pairs

     Returns
     --------
       rr:
        reduction ratio as float value.
  """
    rr = 0.0
    return rr


# -----------------------------------------------------------------------------
# TODO Implement pairs completeness
def pairs_completeness(cand_rec_id_pair_list, true_match_set):
    """Computes the pairs completeness that measures the effectiveness of a blocking technique.

     Pairs completeness is calculated as the number of true matches included in
     the candidate record pairs divided by the number of all true matches.

     Parameters
     ------------
       cand_rec_id_pair_list :
          Dictionary of candidate record pairs generated
                               by a blocking technique
       true_match_set        :
          Set of true matches (record identifier pairs)

      Returns
     --------
       pc:
        pairs completeness as float value.
  """

    pc = 0.0
    return pc


# -----------------------------------------------------------------------------
# TODO Implement pairs quality
def pairs_quality(cand_rec_id_pair_list, true_match_set):
    """Computes the pairs quality that measures the efficiency of a blocking technique.

     Pairs quality is calculated as the number of true matches included in the
     candidate record pairs divided by the number of candidate record pairs
     generated by blocking.

     Parameters
     ------------
       cand_rec_id_pair_list :
          Dictionary of candidate record pairs generated
                               by a blocking technique
       true_match_set        :
          Set of true matches (record identifier pairs)

      Returns
     --------
       pq:
        pairs quality as float value.
  """

    pq = 0.0
    return pq

# -----------------------------------------------------------------------------

# End of program.
