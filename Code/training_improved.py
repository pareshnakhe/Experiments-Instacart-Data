from scipy.stats import beta
import matplotlib
import pandas as pd

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import test
import math


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        # this holds the beta distribution parameters
        # for dept distribution
        self.dept_distr = np.ones((22, 2))

        # this denotes the average number of different departments the user shops from
        self.avg_num_of_unique_depts = 0
        # this denotes the average number of products bought from each dept
        self.avg_num_of_products_per_dept = np.zeros(22)
        # this is a dictionary of the form: dept => prod_distr
        self.product_list = [dict() for x in range(22)]


def predictions(testList, user_dict):
    """
    uses user_dict to make predictions about the set of items bought for each order in testList
    It is important to note here that the threshold of 0.5 for dept_prob and prod_prob is a parameter.
    Change this to fine tune the algorithm behaviour.
    :param testList:
    :param user_dict:
    """

    print 'In predictions...'
    # loop over all orders in testList
    i = 0
    accuracy = 0.0
    accuracy_vol = 0.0
    for order in testList:
        # pred_list is the list of products predicted by the algorithm
        pred_list = list()
        user_id = order[1]
        print user_id

        if user_id not in user_dict:
            print "New User!?"
            exit(1)

        user_obj = user_dict[user_id]
        dept_prob = np.zeros(22)
        for dept_id in xrange(1, 22):
            a = user_obj.dept_distr[dept_id][0]
            b = user_obj.dept_distr[dept_id][1]
            if a <= 0.0 or b <= 0.0:
                print "dept_id: error", a, b
                exit(1)

            # draw a value from the distribution for department dept_id
            dept_prob[dept_id] = beta.rvs(a, b)

        norm_dept_prob = [dept_prob[dept_id] / sum(dept_prob) for dept_id in xrange(1, 22)]

        pred_dept_list = np.random.choice(21, int(math.ceil(user_obj.avg_num_of_unique_depts)) + 2, replace=False,
                                          p=norm_dept_prob)
        pred_dept_list = [pred_dept_list[i] + 1 for i in range(len(pred_dept_list))]
        print 'pred_dept_list: ', pred_dept_list

        # for each dept chosen
        for dept_id in pred_dept_list:
            prod_prob = dict()
            for prod_id, distr_para in user_obj.product_list[dept_id].iteritems():
                a = user_obj.product_list[dept_id][prod_id][0]
                b = user_obj.product_list[dept_id][prod_id][1]
                if a <= 0.0 or b <= 0.0:
                    print "prod_id: error", a, b
                    exit(1)
                prod_prob[prod_id] = beta.rvs(a, b)

            # print 'prod_prob: ', prod_prob
            # if prod_prob dictionary is not empty
            if prod_prob:
                norm_prod_prob = dict()
                for prod_id, rand_var in prod_prob.iteritems():
                    norm_prod_prob[prod_id] = prod_prob[prod_id] / sum(prod_prob.values())

                # print norm_prod_prob
                # print 'norm_prod_prob.keys(): ', norm_prod_prob.keys()
                # print 'norm_prod_prob.values(): ', norm_prod_prob.values()

                pred_prod_list = list(np.random.choice(norm_prod_prob.keys(),
                                                       min(int(math.ceil(
                                                           user_obj.avg_num_of_products_per_dept[dept_id])) + 2,
                                                           len(norm_prod_prob.keys())),
                                                       replace=False, p=norm_prod_prob.values()))
            else:
                pred_prod_list = list()
                pred_prod_list.append('None')

            pred_list.extend(pred_prod_list)
            # exit(1)

        print pred_list, order[2]
        correct_predictions = np.intersect1d(pred_list, order[2])
        print 'correct_predictions', correct_predictions
        accuracy += float(len(correct_predictions)) / len(order[2])
        accuracy_vol += float(len(correct_predictions)) / len(pred_list)
        # i += 1
        # if i >= 5:
        #     exit(1)

    avg_precision = accuracy / len(testList)
    avg_recall = accuracy_vol / len(testList)
    print 'Average Precision:', avg_precision
    print 'Average Recall:', avg_recall
    print 'F1 score:', 2.0*avg_precision*avg_recall / (avg_precision + avg_recall)


order_products_prior = pd.read_csv('Data/order_products__skimmed_train.csv').loc[:, ['order_id', 'product_id']]
products = pd.read_csv('Data/products.csv').loc[:, ['product_id', 'department_id']]
orders = pd.read_csv('Data/orders.csv')
orders_prior = orders.loc[orders['eval_set'] == 'prior', ['order_id', 'user_id']].reset_index()

compact = pd.merge(order_products_prior, products)
compact = pd.merge(compact, orders_prior)
compact = compact.loc[:, ['user_id', 'order_id', 'department_id', 'product_id']]
print compact.head(5)

user_dict = dict()

for user_id in compact.loc[:, 'user_id'].unique():
    print 'user_id:', user_id
    user_data = compact.loc[compact['user_id'] == user_id, ['order_id', 'department_id', 'product_id']]
    no_of_orders = user_data.shape[0]
    # print no_of_orders,

    if user_id not in user_dict:
        user_dict[user_id] = User(user_id)

    user_obj = user_dict[user_id]
    unique_orders = user_data.loc[:, 'order_id'].unique()
    for order in unique_orders:
        # print order
        unique_depts = user_data.loc[user_data['order_id'] == order, 'department_id'].unique()
        user_obj.avg_num_of_unique_depts += len(unique_depts)
        # print user_id, unique_depts

        user_order_data = user_data.loc[user_data['order_id'] == order, ['department_id', 'product_id']]
        for dept_id in unique_depts:
            # print dept_id
            user_obj.dept_distr[dept_id][0] += 1
            # other_depts = [i for i in xrange(1, 22) if i != dept_id]
            for other_dept_id in [i for i in xrange(1, 22) if i != dept_id]:
                user_obj.dept_distr[other_dept_id][1] += 1

            # print user_order_data.loc[user_order_data['department_id'] == dept_id, 'product_id'].values
            unique_prods = user_order_data.loc[user_order_data['department_id'] == dept_id, 'product_id'].unique()
            # print unique_prods
            user_obj.avg_num_of_products_per_dept[dept_id] += len(unique_prods)

            for prod_id in unique_prods:
                # print prod_id
                if prod_id not in user_obj.product_list[dept_id]:
                    user_obj.product_list[dept_id][prod_id] = np.ones(2)

                user_obj.product_list[dept_id][prod_id][0] += 1

    for prod_id in user_obj.product_list[dept_id]:
        user_obj.product_list[dept_id][prod_id][1] += \
            user_obj.avg_num_of_products_per_dept[dept_id] - user_obj.product_list[dept_id][prod_id][0] + 1

    user_obj.avg_num_of_unique_depts /= float(len(unique_orders))
    # print user_id, user_obj.avg_num_of_unique_depts
    for i in xrange(1, 22):
        user_obj.avg_num_of_products_per_dept[i] /= len(unique_orders)
        # print 'dept:', i, user_obj.avg_num_of_products_per_dept[i]

testList = test.createTestList()
predictions(testList, user_dict)
