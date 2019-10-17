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
                  - So average order value is more robust and we can use that.
              b. Avg. order value
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