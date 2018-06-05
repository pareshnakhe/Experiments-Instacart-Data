import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np


def createTestList():
    """
    Creates a data structure to iterate over the test orders.
    These orders are stored in a list of the form: [ order_id, user_id, [list of products] ]

    :return: testList data structure
    """
    print 'Creating testList'

    order_products_test = pd.read_csv('Data/order_products__skimmed_test.csv').loc[:, ['order_id', 'product_id']]
    orders = pd.read_csv('Data/orders.csv')
    orders_test = orders.loc[orders['eval_set'] == 'prior', ['order_id', 'user_id']].reset_index()

    testList = list()

    for order_id in order_products_test.loc[:, 'order_id'].unique():
        orderList = list()
        orderList.append(order_id)
        # print orderList

        user_id = orders_test.loc[orders_test['order_id'] == order_id, 'user_id'].values[0]
        orderList.append(user_id)
        # print orderList

        temp = order_products_test.loc[order_products_test['order_id'] == order_id, 'product_id'].values
        orderList.append(temp)
        # print orderList

        testList.append(orderList)

    return testList


