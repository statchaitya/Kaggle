# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 19:25:35 2019

In this script, 
    1. We look at the problem we are trying to solve
    2. Think about the features we can use
    3. Create data
    4. Explore the features and target relationship
    
@author: cgokh
"""

import pandas as pd
import numpy as np
import gc

train = pd.read_csv("C:/Kaggle/googlemerchandise/data/train_new.csv", encoding = "ISO-8859-1")


'''
Problem: Gstore product manager wants to know the important customer level characteristics that
affect revenue the most

Solution Imagination: AOV. is negatively correlated to # bounces and positively correlated to
                      # page views.

Steps:
    1. Customer Empathy
        - Characteristics indicating intent to buy?
        - Belongs to area having high avg. annual income?
        - Is he/she a repeat buyer?
        - What is the frequency of repetition? - Frequency of past purchases?
        - Has this customer ever came from a direct search/organic channel?
    2. Metrics
        - Since Gstore PM wants to focus on the effect on revenue. Metrics related to rev.
          can be
              a. Total Revenue till date
                  - This metric might be biased because a customer can buy 50 times and give us
                    10000 bucks on the contrary on can buy stuff worth 10000 in 3-4 times if he/she
                    buys costly things.
                  - So average order value per customer is more robust and we can use that.
              b. Avg. order value per customer
                  - Some customers have a very high AOV (16k, 7k, 5.6k etc..)
                  - Most of the distribution revolves around 0
    3. Features
        - Taking input from customer empathy, important features affecting AOV or revenue in general
          maybe
              a. 4-5 categories of avg. annual income of the location
              b. # visits from each channel - multi numeric feature
              c. # visits on day of week - MNF
              d. # pageviews / visit
              e. Total # pageviews
              f. # bounces / visit
              g. Total # bounces
'''

# Creation of metrics defined above in 2

# Total revenue per customer till date

train['totalRevenue'] = train.groupby('fullVisitorId').transactionRevenueNew.transform(np.sum)
train['visitRevenueFlag'] = [1 if i > 0 else 0 for i in list(train['transactionRevenueNew'])]
train['totalOrders'] = train.groupby('fullVisitorId').visitRevenueFlag.transform(np.sum)
train['AOVPerCustomer'] = train['totalRevenue']/train['totalOrders'] 
train['AOVPerCustomer'].fillna(0, inplace=True)


cust_df = train.groupby('fullVisitorId').count()['transactionRevenueNew'].reset_index(name='totalVisits')
new_key = list(range(cust_df.shape[0]))
cust_df['new_cust_id'] = new_key

train = pd.merge(train, cust_df, on = "fullVisitorId")

target_df = train[['new_cust_id', 'AOVPerCustomer']].groupby('new_cust_id').max()['AOVPerCustomer'].reset_index()
cust_df = pd.merge(cust_df, target_df, on="new_cust_id")
# Some customers have a very high AOV (16k, 7k, 5.6k etc..). Should these customers
# ..    be included in the analysis?

# Creating features

# First creating # visits from various categories of categorical features
# Ex: total visits done from browser, mobile, tablet | total organic search visits etc..

def count_category_visits(categorical_variable, category):
    print("Current category is ", category)
    category_newname = category.replace(" ", "_")
    gbdf = train.groupby(['new_cust_id', categorical_variable]).count()['transactionRevenueNew'].reset_index(name= category_newname+"_visits")
    gbdf[categorical_variable] = gbdf[categorical_variable].astype(str)
    gbdf = gbdf[gbdf[categorical_variable] == category]
    gbdf = gbdf[["new_cust_id", category_newname+"_visits"]]
    return gbdf

categorical_variables = ['channelGrouping', 'deviceCategory', 'wday']

for categorical_variable in categorical_variables:
    for category in list(set(train[categorical_variable])):
        print("Executing process for ", categorical_variable)
        print("And category", category)
        gc.collect()
        print(cust_df.shape)
        cust_df = pd.merge(cust_df, count_category_visits(categorical_variable, category), on = "new_cust_id", how="left")

cust_df.fillna(0, inplace=True)

# Now creating the common features such as 


''' Decision tree plot Example '''

from sklearn.tree import DecisionTreeRegressor, export_graphviz
from sklearn import tree
from graphviz import Source

# Need to download graphviz executables to display DT in console
# Shall need below code then
#import os
#os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'

features = [i for i in list(cust_df.columns) if i not in ['fullVisitorId', 'AOVPerCustomer']]

# feature matrix
X = cust_df[features]

# target vector
y = cust_df['AOVPerCustomer']

estimator = DecisionTreeRegressor(criterion='mae')
estimator.fit(X, y)

dot_data = tree.export_graphviz(estimator, out_file='tree.dot', max_depth=5, feature_names=features) 





