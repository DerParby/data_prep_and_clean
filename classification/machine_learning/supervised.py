import numpy
from sklearn.tree import DecisionTreeClassifier, BaseDecisionTree


def train_supervised(sim_vec_dict, true_match_set) -> BaseDecisionTree:
    """
    A classifier method based on a supervised machine learning technique
     (decision tree) which learns from the given similarity vectors and the
     true match status set provided.

    Parameters
    -------------
    sim_vec_dict  :
        Dictionary of record pairs with their identifiers as
                       as keys and their corresponding similarity vectors as
                       values.
    true_match_set :
          Set of true matches (record identifier pairs)

    Returns
    ---------
    decision_tree:
        trained decision tree

  """

    print('Supervised decision tree classification of %d record pairs' % \
          (len(sim_vec_dict)))

    # Generate the training data sets (similarity vectors plus class labels
    # (match or non-match)
    #
    num_train_rec = len(sim_vec_dict)
    num_features = len(list(sim_vec_dict.values())[0])

    print('  Number of training records and features: %d / %d' % \
          (num_train_rec, num_features))

    all_train_data = numpy.zeros([num_train_rec, num_features])
    all_train_class = numpy.zeros(num_train_rec)

    rec_pair_id_list = []

    num_pos = 0
    num_neg = 0
    i = 0
    for (rec_id1, rec_id2) in sim_vec_dict:
        rec_pair_id_list.append((rec_id1, rec_id2))
        sim_vec = sim_vec_dict[(rec_id1, rec_id2)]

        all_train_data[:][i] = sim_vec

        if (rec_id1, rec_id2) in true_match_set or (rec_id2, rec_id1) in true_match_set:
            all_train_class[i] = 1.0
            num_pos += 1
        else:
            all_train_class[i] = 0.0
            num_neg += 1
        i += 1
    print('Number of positive and negative training records: %d / %d' % \
          (num_pos, num_neg))
    decision_tree = DecisionTreeClassifier()
    decision_tree = decision_tree.fit(all_train_data, all_train_class)
    return decision_tree


def classify_record_pairs(sim_vec_dict, decision_tree: BaseDecisionTree):
    """
    Predicts for each record pair with its similarity vector of the dictionary the class match or non-match
    :param sim_vec_dict: Dictionary of record pairs with their identifiers as
                       as keys and their corresponding similarity vectors as
                       values.
    :param decision_tree: trained model
    :return: set of matches, set of non-matches
    """
    class_match_set = set()
    class_nonmatch_set = set()
    num_test_rec = len(sim_vec_dict)
    num_features = len(list(sim_vec_dict.values())[0])
    test_data = numpy.zeros([num_test_rec, num_features])
    rec_pair_id_list = []
    i = 0
    for (rec_id1, rec_id2) in sim_vec_dict:
        rec_pair_id_list.append((rec_id1, rec_id2))
        sim_vec = sim_vec_dict[(rec_id1, rec_id2)]
        test_data[:][i] = sim_vec
        i += 1
    class_predict = decision_tree.predict(test_data)
    for i in range(len(rec_pair_id_list)):
        rec_id_pair = rec_pair_id_list[i]
        if class_predict[i] == 1:
            class_match_set.add(rec_id_pair)
        else:
            class_nonmatch_set.add(rec_id_pair)
    return class_match_set, class_nonmatch_set
