from random import Random

import numpy as np
from numpy import ndarray


def select_blocking_keys(rec_dict_a, rec_dict_b, blocking_key_candidates, ground_truth_pairs, training_size,
                         eps, max_block_size_ratio):
    """
    This method determines a list of blocking keys that is used for disjunctive blocking based on a candidate list. The method
    iteratively selects a blocking Key candidate to the result processing the following steps.
      - The candidate list is filtered by the max_block_size_ratio.
      - We compute for each remaining blocking key the Fisher score.
      - After that, we select and add the blocking key to the final result with the maximum Fisher score, and if at least one new record pair is
        covered by it.

    The procedure terminates, if the number of uncovered record pairs of M is smaller than eps * |M|

    Parameters
    -----------
    rec_dict_a:
       record dictionary with rec id and list of value pairs for data data source A
     rec_dict_b:
        record dictionary with rec id and list of value pairs for data data source B
     blocking_key_candidates:
         list of blocking key candidates
     ground_truth_pairs:
        set of real matches
     training_size:
        number of positive training samples
     eps:
       allowed ratio of uncovered record pairs
     max_block_size_ratio:
       ratio of maximum block size regarding the total number of records (differs from the original work)

    Returns
    ----------
     final_bks:
         list of blocking key for a DNF blocking scheme
    """
    positive_pairs, negative_pairs = generate_samples(rec_dict_a, rec_dict_b, ground_truth_pairs, training_size)
    number_of_uncovered_recs = eps * training_size
    max_block_size = max_block_size_ratio * max(len(rec_dict_a), len(rec_dict_a))
    max_block_sizes = get_max_block_size(rec_dict_a, rec_dict_b, blocking_key_candidates)
    new_filtered_candidates = []
    for index, bk in enumerate(blocking_key_candidates):
        if max_block_sizes[index] < max_block_size:
            new_filtered_candidates.append(blocking_key_candidates[index])
            
    print(f"Original # blocking keys: {len(blocking_key_candidates)}")
    print(f"Remaining after filtering: {len(new_filtered_candidates)}")
    pf_vectors = generate_feature_vectors(rec_dict_a, rec_dict_b, positive_pairs, new_filtered_candidates)
    nf_vectors = generate_feature_vectors(rec_dict_a, rec_dict_b, negative_pairs, new_filtered_candidates)
    fisher_scores = compute_fisher_score(pf_vectors, nf_vectors)
    print(f"fisher score: {fisher_scores}")
    candidates_score_list = list(zip([index for index in range(len(new_filtered_candidates))], fisher_scores.tolist()))
    candidates_score_list = sorted(candidates_score_list, key=lambda cand: cand[1], reverse=True)
    covered_rec_pairs = set()
    final_bks = []
    for bk_index, score in candidates_score_list:
        indices = np.where(pf_vectors[:, bk_index] == 1)
        indices = set(indices[0])
        # check if more matches are covered than before
        diff = indices.difference(covered_rec_pairs)
        if len(diff) > 0:
            covered_rec_pairs = covered_rec_pairs.union(diff)
            final_bks.append(new_filtered_candidates[bk_index])
        if training_size - len(covered_rec_pairs) < number_of_uncovered_recs:
            break
    return final_bks


def get_max_block_size(rec_dict_a, rec_dict_b, blocking_key_candidates):
    max_block_size_list = []
    for bf, a in blocking_key_candidates:
        block_dict = {}
        for rec_id, rec_values in rec_dict_a.items():
            rec_bkv = bf(rec_values, a)
            if rec_bkv in block_dict:
                rec_id_list = block_dict[rec_bkv]
                rec_id_list.append(rec_id)
            else:
                rec_id_list = [rec_id]
            block_dict[rec_bkv] = rec_id_list  # Store the new block
        max_block_size = max([len(rec_list) for rec_list in block_dict.values()])
        max_block_size_list.append(max_block_size)
    att_index = 0
    for bf, a in blocking_key_candidates:
        block_dict = {}
        for rec_id, rec_values in rec_dict_b.items():
            rec_bkv = bf(rec_values, a)
            if rec_bkv in block_dict:
                rec_id_list = block_dict[rec_bkv]
                rec_id_list.append(rec_id)
            else:
                rec_id_list = [rec_id]
            block_dict[rec_bkv] = rec_id_list  # Store the new block
        max_block_size = max([len(rec_list) for rec_list in block_dict.values()])
        max_block_size_list[att_index] = max(max_block_size_list[att_index], max_block_size)
        att_index += 1
    return max_block_size_list


def generate_samples(rec_dict_a, rec_dict_b, ground_truth_pairs, training_size):
    """
    This method generates a training data set consisting of record pairs classified as match and non-match.

    Parameters
    ----------
    rec_dict_a:
         record dictionary with rec id and list of value pairs for data data source A
    rec_dict_b:
         record dictionary with rec id and list of value pairs for data data source B
    ground_truth_pairs:
        set of true matches
    training_size:
       number of true matches

    Returns
    ---------
    training_data_set:
       set of matches, and set of non-matches
    """
    records_A = list(rec_dict_a.keys())
    r = Random(42)
    r.shuffle(records_A)
    records_B = list(rec_dict_b.keys())
    r.shuffle(records_B)
    negative_pairs = set(zip(records_A, records_B))
    negative_pairs = set(list(negative_pairs.difference(ground_truth_pairs))[:training_size])
    positive_pairs = set(list(ground_truth_pairs)[:training_size])
    return positive_pairs, negative_pairs


def generate_feature_vectors(rec_dict_a, rec_dict_b, pair_set, blocking_key_candidates):
    """
    Generates a binary matrix where entry (i, j) = 1 if the j-th blocking key gives same value for the i-th pair.
    """
    feature_vector_array = np.zeros((len(pair_set), len(blocking_key_candidates)))
    pair_list = list(pair_set)

    for i, (id_a, id_b) in enumerate(pair_list):
        rec_a = rec_dict_a[id_a]
        rec_b = rec_dict_b[id_b]
        for j, (bf, attr) in enumerate(blocking_key_candidates):
            if bf(rec_a, attr) == bf(rec_b, attr):
                feature_vector_array[i, j] = 1
    return feature_vector_array


def compute_fisher_score(pf_vectors: ndarray, nf_vectors: ndarray):
    """
    Computes the Fisher score for each blocking key.
    """
    mean_pos = np.mean(pf_vectors, axis=0)
    mean_neg = np.mean(nf_vectors, axis=0)
    var_pos = np.var(pf_vectors, axis=0)
    var_neg = np.var(nf_vectors, axis=0)

    numerator = np.square(mean_pos - mean_neg)
    denominator = var_pos + var_neg

    with np.errstate(divide='ignore', invalid='ignore'):
        fisher_scores = np.divide(numerator, denominator)
        fisher_scores[np.isnan(fisher_scores)] = 0.0

    return fisher_scores