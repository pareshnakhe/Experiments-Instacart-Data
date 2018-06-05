import pandas as pd
from scipy.stats import beta
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
import test


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        # this holds the beta distribution parameters
        # for dept distribution
        self.dept_distr = np.ones((21, 2))
        # this is a dictionary of the form: dept => prod_distr
        self.product_list = [dict() for x in range(21)]


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
        i=0
        accuracy = 0.0
        for order in testList:
            # pred_list is the list of products predicted by the algorithm
            pred_list = list()
            user_id = order[1]
            print user_id

            if user_id not in user_dict:
                print "New User!?"
                exit(1)

            user_obj = user_dict[user_id]
            for dept_id in xrange(0, 21):
                a = user_obj.dept_distr[dept_id][0]
                b = user_obj.dept_distr[dept_id][1]
                if a <= 0.0 or b <= 0.0:
                    print "dept_id: error", a, b
                    exit(1)

                # draw a value from the distribution for department dept_id
                dept_prob = beta.rvs(a, b)
                # print 'dept_prob: ', dept_id, dept_prob
                # print dept_prob
                # continue to product distributions if probability of choosing the department is >=0.5
                if dept_prob >= 0.10:
                    for prod_id, distr_para in user_obj.product_list[dept_id].iteritems():
                        a = user_obj.product_list[dept_id][prod_id][0]
                        b = user_obj.product_list[dept_id][prod_id][1]
                        if a <= 0.0 or b <= 0.0:
                            print "prod_id: error", a, b
                            exit(1)
                        prod_prob = beta.rvs(a, b)
                        # print 'prod_prob: ', prod_id, prod_prob
                        # if prob of choosing a product greater than 0.5, add it to predicted list
                        if prod_prob >= 0.10:
                            pred_list.append(prod_id)

            print pred_list, order[2]
            correct_predictions = np.intersect1d(pred_list, order[2])
            print correct_predictions
            accuracy += float(len(correct_predictions)) / len(order[2])
            # i += 1
            # if i >= 5:
            #     break
        print 'Average accuracy:', accuracy / len(testList)


# read data from the respective files and create a compact view for training the model
# resulting view is of the form: ['user_id', 'department_id', 'product_id']

order_products_prior = pd.read_csv('Data/order_products__skimmed_train.csv').loc[:, ['order_id', 'product_id']]
products = pd.read_csv('Data/products.csv').loc[:, ['product_id', 'department_id']]
orders = pd.read_csv('Data/orders.csv')
orders_prior = orders.loc[orders['eval_set'] == 'prior', ['order_id', 'user_id']].reset_index()

compact = pd.merge(order_products_prior, products)
compact = pd.merge(compact, orders_prior)
compact = compact.loc[:, ['user_id', 'department_id', 'product_id']]
print compact.head(2)


# Approach based on beta distribution

user_dict = dict()

for user_id in compact.loc[:, 'user_id'].unique():
    print 'user_id:', user_id
    temp = compact.loc[compact['user_id'] == user_id, ['department_id', 'product_id']]
    no_of_orders = temp.shape[0]
    # print no_of_orders,

    if user_id not in user_dict:
        user_dict[user_id] = User(user_id)

    user_obj = user_dict[user_id]
    for dept_id in temp.loc[:, 'department_id'].values:
        user_obj.dept_distr[dept_id-1][0] += 1

    for dept_id in xrange(0, 21):
        user_obj.dept_distr[dept_id][1] += no_of_orders - user_obj.dept_distr[dept_id][0] + 1

        # compute the alpha beta parameters also for the individual products in a dept
        # print 'dept_id:', dept_id
        product_info = temp.loc[temp['department_id'] == dept_id, 'product_id']
        no_of_product_orders = product_info.shape[0]
        # print no_of_product_orders

        for prod_id in product_info.values:
            if prod_id not in user_obj.product_list[dept_id]:
                user_obj.product_list[dept_id][prod_id] = np.ones(2)

            user_obj.product_list[dept_id][prod_id][0] += 1

        for prod_id in user_obj.product_list[dept_id]:
            user_obj.product_list[dept_id][prod_id][1] += \
                no_of_product_orders - user_obj.product_list[dept_id][prod_id][0] + 1

            # debugging step
            if user_obj.product_list[dept_id][prod_id][1] <= 0.0:
                print "user_obj.product_list[dept_id][prod_id][0]", user_obj.product_list[dept_id][prod_id][0]
                print "user_obj.product_list[dept_id][prod_id][1]", user_obj.product_list[dept_id][prod_id][1]
                print "Product_info.values: ", product_info.values
                print "no_of_product_orders: ", no_of_product_orders
                print "user_obj.product_list[dept_id][prod_id]", user_obj.product_list[dept_id][prod_id]
                exit(1)

# ============================================================================================================
testList = test.createTestList()
predictions(testList, user_dict)
