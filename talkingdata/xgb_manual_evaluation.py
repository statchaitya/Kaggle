# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 13:50:37 2018

@author: cgokh
"""
import time
model_start = time.time()
import gc
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.cross_validation import train_test_split
# Change this for validation with 10% from train
#is_valid = True

data_import_start = time.time()
path = 'C:/Kaggle/talkingdata/'


def timeFeatures(df):
    # Make some new features with click_time column
    df['datetime'] = pd.to_datetime(df['click_time'])
    df['dow']      = df['datetime'].dt.dayofweek
    df["doy"]      = df["datetime"].dt.dayofyear
    #df["dteom"]    = df["datetime"].dt.daysinmonth - df["datetime"].dt.day
    df.drop(['click_time', 'datetime'], axis=1, inplace=True)
    return df

train_columns = ['ip', 'app', 'device', 'os', 'channel', 'click_time', 'is_attributed']
test_columns  = ['ip', 'app', 'device', 'os', 'channel', 'click_time', 'click_id']
dtypes = {
        'ip'            : 'uint32',
        'app'           : 'uint16',
        'device'        : 'uint16',
        'os'            : 'uint16',
        'channel'       : 'uint16',
        'is_attributed' : 'uint8',
        'click_id'      : 'uint32'
        }

# Picking up train data from multiple non-adjacent slices

# Following train file is for skip

'''
temp_task = ['ip','app','is_attributed']
train = pd.read_csv(path+"train.csv", usecols=temp_task, dtype=dtypes)
app_count = train.groupby(['app','is_attributed']).count()['ip'].reset_index()
app_count.columns = ['app','is_attributed','clicks']
app_count.head()
app_dloads = app_count[app_count['is_attributed'] == 1]
app_dloads.drop('is_attributed', axis=1, inplace=True)
del train
'''

#41m
#train = pd.read_csv(path+"train.csv", nrows=41000000, usecols=train_columns, dtype=dtypes)
skip = pd.read_csv(path+"skip.csv", usecols=['skip1'])
train = pd.read_csv(path+"train.csv", skiprows=skip['skip1'], usecols=train_columns, dtype=dtypes)
del skip

#data_import_finish = time.time()


train = train[:40000000]
                 
test = pd.read_csv(path+"test.csv", usecols=test_columns, dtype=dtypes)
gc.collect()


y = train['is_attributed']
train.drop(['is_attributed'], axis=1, inplace=True)

sub = pd.DataFrame()
sub['click_id'] = test['click_id'].astype('int')
test.drop(['click_id'], axis=1, inplace=True)
gc.collect()

#y_dev = dev_set['is_attributed']
#dev_set.drop(['is_attributed'], axis=1, inplace=True)

nrow_train = train.shape[0]
#nrow_dev = dev_set.shape[0]
merge = pd.concat([train, test])
del train, test
gc.collect()

# importing data to be merged
import os
os.chdir('C:/Kaggle/talkingdata/features/')

app_dloads_yes = pd.read_csv("app_dloads_yes.csv")
app_dloads_no = pd.read_csv("app_dloads_no.csv")
channel_dloads_yes = pd.read_csv("channel_dloads_yes.csv")
channel_dloads_no = pd.read_csv("channel_dloads_no.csv")
os_dloads_yes = pd.read_csv("os_dloads_yes.csv")
os_dloads_no = pd.read_csv("os_dloads_no.csv")

app_dloads_no.columns = ['app','clicks_app_is_atr_0']

merge = pd.merge(merge, app_dloads_yes, on='app', how='left', sort=False)
merge['clicks_app_is_atr_1'].fillna(0, inplace=True)
merge['clicks_app_is_atr_1'] = merge['clicks_app_is_atr_1'].astype('uint16')

merge = pd.merge(merge, app_dloads_no, on='app', how='left', sort=False)
merge['clicks_app_is_atr_0'].fillna(0, inplace=True)
merge['clicks_app_is_atr_0'] = merge['clicks_app_is_atr_0'].astype('uint16')


channel_dloads_no.columns = ['channel','clicks_channel_is_atr_0']

merge = pd.merge(merge, channel_dloads_yes, on='channel', how='left', sort=False)
merge['clicks_channel_is_atr_1'].fillna(0, inplace=True)
merge['clicks_channel_is_atr_1'] = merge['clicks_channel_is_atr_1'].astype('uint16')

merge = pd.merge(merge, channel_dloads_no, on='channel', how='left', sort=False)
merge['clicks_channel_is_atr_0'].fillna(0, inplace=True)
merge['clicks_channel_is_atr_0'] = merge['clicks_channel_is_atr_1'].astype('uint16')


os_dloads_no.columns = ['os','clicks_os_is_atr_0']

merge = pd.merge(merge, os_dloads_yes, on='os', how='left', sort=False)
merge['clicks_os_is_atr_1'].fillna(0, inplace=True)
merge['clicks_os_is_atr_1'] = merge['clicks_os_is_atr_1'].astype('uint16')

merge = pd.merge(merge, os_dloads_no, on='os', how='left', sort=False)
merge['clicks_os_is_atr_0'].fillna(0, inplace=True)
merge['clicks_os_is_atr_0'] = merge['clicks_os_is_atr_1'].astype('uint16')

ip_count = merge.groupby(['ip'])['channel'].count().reset_index()
ip_count.columns = ['ip', 'clicks_by_ip']
merge = pd.merge(merge, ip_count, on='ip', how='left', sort=False)
merge['clicks_by_ip'] = merge['clicks_by_ip'].astype('uint16')

train = merge[:nrow_train]
#dev_set = merge[nrow_train+1:nrow_train+1+nrow_dev]
#test = merge[nrow_train+1+nrow_dev:]

del merge
gc.collect()

train = timeFeatures(train)
#dev_set = timeFeatures(dev_set)
gc.collect()

# TRAIN-DEV APPROACH
params = {'eta': 0.2,
          'tree_method': "hist",
          'grow_policy': "lossguide",
          'max_leaves': 1400,  
          'max_depth': 0, 
          'subsample': 0.95, 
          'colsample_bytree': 0.65, 
          'colsample_bylevel':0.7,
          'min_child_weight':0.6,
          'alpha':4,
          'objective': 'binary:logistic', 
          'scale_pos_weight':9,
          'eval_metric': 'auc', 
          'nthread':8,
          'random_state': 99, 
          'silent': True}


is_valid = False
if (is_valid == True):
    # Get 10% of train dataset to use as validation
    x1, x2, y1, y2 = train_test_split(train, y, test_size=0.1, random_state=99)
    dtrain = xgb.DMatrix(x1, y1)
    dvalid = xgb.DMatrix(x2, y2)
    del x1, y1, x2, y2 
    gc.collect()
    watchlist = [(dtrain, 'train'), (dvalid, 'valid')]
    model = xgb.train(params, dtrain, 29, watchlist, maximize=True, early_stopping_rounds = 15, verbose_eval=1)
    del dvalid
else:
    dtrain = xgb.DMatrix(train, y)
    del train, y
    gc.collect()
    watchlist = [(dtrain, 'train')]
    model = xgb.train(params, dtrain, 29, watchlist, maximize=True, verbose_eval=1)


#del dtrain
#gc.collect()
#del model


# CROSS-VALIDATION APPROACH

#cvresult = xgb.cv(params, dtrain, num_boost_round=30, nfold=5,
#                  metrics='auc', early_stopping_rounds=10)


# PREDICTIONS on TEST
del dtrain
gc.collect()
test = pd.read_csv(path+"test.csv", usecols=test_columns, dtype=dtypes)
test = pd.merge(test, ip_count, on='ip', how='left', sort=False)
test['clicks_by_ip'] = test['clicks_by_ip'].astype('uint16')
del ip_count
gc.collect()
test = pd.merge(test, app_dloads, on='app', how='left', sort=False)
test['clicks'].fillna(0, inplace=True)
test = timeFeatures(test)
test.drop(['click_id', 'ip'], axis=1, inplace=True)
dtest = xgb.DMatrix(test)
del test
gc.collect()

# Save the predictions
sub['is_attributed'] = model.predict(dtest)
sub.to_csv('sub_skip3.csv',index=False)
model_end = time.time()
'''
plot importance
'''
from xgboost import plot_importance
import matplotlib.pyplot as plt
plot_importance(model)
plt.gcf().savefig('feature_importance_xgb.png')



'''
Code to delete everything from the environment
Like rm(list=ls())

for name in dir():
    if not name.startswith('_'):
        del globals()[name]
'''



eta_grid = [0.6,0.5,0.4,0.3,0.2,0.1]

def tune_eta(eta_grid):
    x1, x2, y1, y2 = train_test_split(train, y, test_size=0.1, random_state=99)
    dtrain = xgb.DMatrix(x1, y1)
    dvalid = xgb.DMatrix(x2, y2)
    del x1, y1, x2, y2 
    gc.collect()
    watchlist = [(dtrain, 'train'), (dvalid, 'valid')]
    
    eta_tuned = pd.DataFrame()
    eta_tuned['eta_values'] = eta_grid
    
    best_iteration = []
    best_score = []
    
    for i in range(0,len(eta_grid)):
        params = {'eta': eta_grid[i],
                  'tree_method': "hist",
                  'grow_policy': "lossguide",
                  'max_leaves': 1400,  
                  'max_depth': 0, 
                  'subsample': 0.75, 
                  'colsample_bytree': 0.7, 
                  'colsample_bylevel':0.7,
                  'min_child_weight':0,
                  'alpha':4,
                  'objective': 'binary:logistic', 
                  'scale_pos_weight':9,
                  'eval_metric': 'auc', 
                  'nthread':8,
                  'random_state': 99, 
                  'silent': True}
        model = xgb.train(params, dtrain, 2500, watchlist, maximize=True, early_stopping_rounds = 15, verbose_eval=1)
                
        best_iteration.append(model.best_iteration)
        best_score.append(model.best_score)
        
        del model
        gc.collect()
    
    eta_tuned['best_iteration'] = best_iteration
    eta_tuned['best_score']= best_score
    
    return eta_tuned
        
        
eta_tuned = tune_eta(eta_grid)

eta_tuned


############################################################################################


sub_sample_grid = [0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1]

def tune_subsample(sub_sample_grid):
    x1, x2, y1, y2 = train_test_split(train, y, test_size=0.1, random_state=99)
    dtrain = xgb.DMatrix(x1, y1)
    dvalid = xgb.DMatrix(x2, y2)
    del x1, y1, x2, y2 
    gc.collect()
    watchlist = [(dtrain, 'train'), (dvalid, 'valid')]
    
    subsample_tuned = pd.DataFrame()
    subsample_tuned['sub_sample_values'] = sub_sample_grid
    
    best_iteration = []
    best_score = []
    
    for i in range(0,len(sub_sample_grid)):
        params = {'eta': 0.2,
                  'tree_method': "hist",
                  'grow_policy': "lossguide",
                  'max_leaves': 1400,  
                  'max_depth': 0, 
                  'subsample': sub_sample_grid[i], 
                  'colsample_bytree': 0.7, #can be 1
                  'colsample_bylevel':0.7, #can be 1
                  'min_child_weight':0,
                  'alpha':4,
                  'objective': 'binary:logistic', 
                  'scale_pos_weight':9,
                  'eval_metric': 'auc', 
                  'nthread':8,
                  'random_state': 99, 
                  'silent': True}
        model = xgb.train(params, dtrain, 30, watchlist, maximize=True, early_stopping_rounds = 15, verbose_eval=1)
                
        best_iteration.append(model.best_iteration)
        best_score.append(model.best_score)
        
        del model
        gc.collect()
    
    subsample_tuned['best_iteration'] = best_iteration
    subsample_tuned['best_score']= best_score
    
    return subsample_tuned
        
        
subsample_tuned = tune_subsample(sub_sample_grid)
subsample_tuned.to_csv('subsample_tuned.csv',index=False)

############################################################################################

colsample_bt_grid = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]

def tune_colsamplebt(colsample_bt_grid):
    x1, x2, y1, y2 = train_test_split(train, y, test_size=0.1, random_state=99)
    dtrain = xgb.DMatrix(x1, y1)
    dvalid = xgb.DMatrix(x2, y2)
    del x1, y1, x2, y2 
    gc.collect()
    watchlist = [(dtrain, 'train'), (dvalid, 'valid')]
    
    colsamplebt_tuned = pd.DataFrame()
    colsamplebt_tuned['colsample_bt_values'] = colsample_bt_grid
    
    best_iteration = []
    best_score = []
    
    for i in range(0,len(colsample_bt_grid)):
        params = {'eta': 0.2,
                  'tree_method': "hist",
                  'grow_policy': "lossguide",
                  'max_leaves': 1400,  
                  'max_depth': 0, 
                  'subsample': 0.75, 
                  'colsample_bytree': colsample_bt_grid[i], #can be 1
                  'colsample_bylevel':0.7, #can be 1
                  'min_child_weight':0,
                  'alpha':4,
                  'objective': 'binary:logistic', 
                  'scale_pos_weight':9,
                  'eval_metric': 'auc', 
                  'nthread':8,
                  'random_state': 99, 
                  'silent': True}
        model = xgb.train(params, dtrain, 30, watchlist, maximize=True, early_stopping_rounds = 15, verbose_eval=1)
                
        best_iteration.append(model.best_iteration)
        best_score.append(model.best_score)
        
        del model
        gc.collect()
    
    colsamplebt_tuned['best_iteration'] = best_iteration
    colsamplebt_tuned['best_score']= best_score
    
    return colsamplebt_tuned
        
        
colsamplebt_tuned = tune_colsamplebt(colsample_bt_grid)
colsamplebt_tuned.to_csv('colsamplebt_tuned.csv',index=False)


colsamplebt_tuned
subsample_tuned

############################################################################################


min_child_wt_grid = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

def tune_minchildwt(min_child_wt_grid):
    x1, x2, y1, y2 = train_test_split(train, y, test_size=0.1, random_state=99)
    dtrain = xgb.DMatrix(x1, y1)
    dvalid = xgb.DMatrix(x2, y2)
    del x1, y1, x2, y2 
    gc.collect()
    watchlist = [(dtrain, 'train'), (dvalid, 'valid')]
    
    minchildwt_tuned = pd.DataFrame()
    minchildwt_tuned['min_child_wt_values'] = min_child_wt_grid
    
    best_iteration = []
    best_score = []
    
    for i in range(0,len(min_child_wt_grid)):
        params = {'eta': 0.2,
                  'tree_method': "hist",
                  'grow_policy': "lossguide",
                  'max_leaves': 1400,  
                  'max_depth': 0, 
                  'subsample': 0.95, 
                  'colsample_bytree': 0.65, #can be 1
                  'colsample_bylevel':0.7, #can be 1
                  'min_child_weight':min_child_wt_grid[i],
                  'alpha':4,
                  'objective': 'binary:logistic', 
                  'scale_pos_weight':9,
                  'eval_metric': 'auc', 
                  'nthread':8,
                  'random_state': 99, 
                  'silent': True}
        model = xgb.train(params, dtrain, 100, watchlist, maximize=True, early_stopping_rounds = 15, verbose_eval=1)
                
        best_iteration.append(model.best_iteration)
        best_score.append(model.best_score)
        
        del model
        gc.collect()
    
    minchildwt_tuned['best_iteration'] = best_iteration
    minchildwt_tuned['best_score']= best_score
    
    return minchildwt_tuned
        
        
minchildwt_tuned = tune_minchildwt(min_child_wt_grid)
minchildwt_tuned.to_csv('minchildwt_tuned.csv',index=False)