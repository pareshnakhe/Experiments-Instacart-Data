import pandas as pd
import random
from scipy.stats import beta
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

"""
The code snippet is to make the data set smaller.
(On my machine, it was taking hours to run my algorithm with the original data set)

From Data/orders.csv I have picked only orders from users with total number of orders at least 99.
These orders are then matched with those in Data/order_products__prior.csv and
saved as Data/order_products__skimmed.csv.

This data set is further subdivided into training and testing sets and stored in
Data/order_products__skimmed_test and Data/order_products__skimmed_train respectively.


# of users: 1374
# of orders: 136026
"""

# ======================================================================
# Data cleaning
# snippet to filter orders from user who have ordered at least 99 times
data = pd.DataFrame()
data = pd.read_csv('Data/orders.csv')
data = data.loc[data['eval_set'] == 'prior', ['order_id', 'user_id']]

distr = data.groupby('user_id').count()
# print distr, distr['order_id'].values, distr.index.values
trimmed_data = pd.DataFrame({'order_count': distr['order_id'].values, 'user_id': distr.index.values})

# high_order_users = trimmed_data.loc[trimmed_data['order_count'] >= 99, 'user_id'].values
high_order_users = trimmed_data.loc[trimmed_data['order_count'] >= 99, :]
print type(high_order_users), high_order_users.head()
high_order_users = high_order_users.loc[high_order_users['user_id'] % 2 == 0, 'user_id'].values
print 'Number of users:', len(high_order_users)
# exit(1)

high_order_data = data.loc[data['user_id'].isin(high_order_users)]
print high_order_data.shape
# exit(1)
order_products_prior = pd.read_csv('Data/order_products__prior.csv').loc[:, ['order_id', 'product_id']]
order_products_skimmed = order_products_prior.loc[order_products_prior['order_id'].isin(high_order_data['order_id'].values)]
# print order_products_skimmed.shape
# order_products_skimmed.to_csv('Data/order_products__skimmed.csv')


# split order_products_skimmed into training and testing sets
compl_order_list = order_products_skimmed['order_id'].unique()
no_of_orders = len(compl_order_list)

# draw 20000 random indices for orders
rand_set = random.sample(xrange(no_of_orders), 7500)

# separating orders based on the random sample of indices generated above
testOrders = [compl_order_list[index] for index in rand_set]
trainOrders = [compl_order_list[index] for index in range(len(compl_order_list)) if index not in rand_set]
print len(trainOrders)

order_products_skimmed_test = order_products_skimmed.loc[order_products_skimmed['order_id'].isin(testOrders)]
order_products_skimmed_test.to_csv('Data/order_products__skimmed_test.csv')

order_products_skimmed_train = order_products_skimmed.loc[order_products_skimmed['order_id'].isin(trainOrders)]
order_products_skimmed_train.to_csv('Data/order_products__skimmed_train.csv')
exit(1)