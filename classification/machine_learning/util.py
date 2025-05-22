import random
from collections import defaultdict


def kfold_split(sim_vec_dict: dict[(str, str):list[float]], true_match_set: set, k: int, seed=37) -> list[
    tuple[dict, dict, set, int]]:
    """
    Generate k-fold splits from a dictionary, returning a list of tuples containing
    training and test dictionaries for each fold.

    Parameters
    ------------
    sim_vec_dict:
            Input dictionary to be split into folds
    true_match_set:
        set of true matches
    k:
            Number of folds to generate (must be >= 2)
    seed:
        seed

    Returns
    --------
    train_test_folds:
        List of (train_dict, test_dict, ground_truth_subset, all_comparisons) tuples for each fold
    """
    random.seed(seed)
    non_matching_pairs = dict(sim_vec_dict)
    folds = [defaultdict(list) for i in range(k)]
    true_match_list = list(true_match_set)
    random.shuffle(true_match_list)
    index = 0
    for p in true_match_list:
        if p in non_matching_pairs:
            folds[index % k][p] = non_matching_pairs[p]
            index += 1
            del non_matching_pairs[p]
    for i, p in enumerate(list(non_matching_pairs.keys())):
        folds[i % k][p] = non_matching_pairs[p]
    train_test_folds = []
    for i in range(k):
        test_dict = dict(folds[i])
        gt_subset, all_comparisons = generate_subset(true_match_set, list(test_dict.items()))
        train_dict = {k: v for rest, d in enumerate(folds) if rest != i for k, v in d.items()}
        train_test_folds.append((train_dict, test_dict, gt_subset, all_comparisons))
    return train_test_folds


def generate_subset(true_matches, test_pairs: list):
    gt_subset = set()
    recs_a = set([item[0][0] for item in test_pairs])
    recs_b = set([item[0][1] for item in test_pairs])
    for p in true_matches:
        if p[0] in recs_a and p[1] in recs_b:
            gt_subset.add(p)
    return gt_subset, len(recs_a) * len(recs_b)
