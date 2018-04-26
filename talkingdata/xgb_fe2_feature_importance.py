# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 13:55:14 2018

Simple FE2 model on 30m rows
Aim: Run model. Check feature importance. Removed undesirable features.
Re-run with new reduced feature set and check score.

@author: cgokh
"""
import time
start_time = time.time()
import gc
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.cross_validation import train_test_split

dtypes = {
        'ip'            : 'uint32',
        'app'           : 'uint16',
        'device'        : 'uint16',
        'os'            : 'uint16',
        'channel'       : 'uint16',
        'is_attributed' : 'uint8',
        'click_id'      : 'uint32'
        }

path = 'C:/Kaggle/talkingdata/'

#train_rows = 184903890
#model_train_rows = 30000000
#skip = train_rows - model_train_rows
train_columns = ['ip', 'app', 'device', 'os', 'channel', 'click_time','is_attributed']
#train = pd.read_csv(path+"train.csv",  skiprows = range(1,skip+1), usecols = train_columns, dtype=dtypes)
train = pd.read_csv(path+"train.csv", usecols = train_columns, nrows = 30000000, dtype=dtypes)
test_columns = train_columns[:-1]
test = pd.read_csv(path+"test.csv", usecols = test_columns, dtype=dtypes)
#train = pd.read_csv(path+"train.csv",  nrows=10000000, usecols = train_columns, dtype=dtypes)
print("train data read. train data shape is", train.shape)

nrow_train = train.shape[0]
merge = pd.concat([train,test])
del train, test
gc.collect()

def timeFeatures(df):
    # Make some new features with click_time column
    df['datetime'] = pd.to_datetime(df['click_time'])
    df['wday'] = df['datetime'].dt.dayofweek
    df["hour"] = df["datetime"].dt.hour
    #df["dteom"]    = df["datetime"].dt.daysinmonth - df["datetime"].dt.day
    df.drop(['click_time', 'datetime'], axis=1, inplace=True)
    return df


print("Starting feature engineering")
def feature_engineering_2(df):
    # HOUR AND DAY OF WEEK
    df['datetime'] = pd.to_datetime(df['click_time'])
    df['wday'] = df['datetime'].dt.dayofweek
    df["hour"] = df["datetime"].dt.hour
    df.drop(['click_time', 'datetime'], axis=1, inplace=True)
    
    # Some info from test
    #most_freq_hours_in_test_data = [4,5,9,10,13,14]
    #least_freq_hours_in_test_data = [6,11,15]
        
    nu_apps_ip = df.groupby(['ip'])['app'].nunique().reset_index()
    nu_apps_ip.columns = ['ip', 'nu_apps_ip']
    #df = pd.merge(df, nu_apps_ip, on='ip', how='left', sort=False)
    #df['nu_apps_ip'] = df['nu_apps_ip'].astype('uint16')
    print("Feature 1 done")
    # Number of clicks for a particular IP,DAY,DIFFERENT TIMES OF DAY
    
    nu_channels_ip = df.groupby(['ip'])['channel'].nunique().reset_index()
    nu_channels_ip.columns = ['ip', 'nu_channels_ip']
    #df = pd.merge(df, nu_channels_ip, on='ip', how='left', sort=False)
    #df['nu_channels_ip'] = df['nu_channels_ip'].astype('uint16')
    print("Feature 3 done")
    
    nu_os_ip = df.groupby(['ip'])['os'].nunique().reset_index()
    nu_os_ip.columns = ['ip', 'nu_os_ip']
    #df = pd.merge(df, nu_os_ip, on='ip', how='left', sort=False)
    #df['nu_os_ip'] = df['nu_os_ip'].astype('uint16')
    print("Feature 4 done")
    
    dloads_os = df.groupby(['os','is_attributed'])['channel'].count().reset_index()
    dloads_os.columns = ['os','is_attributed','dloads_os']
    dloads_os = dloads_os[dloads_os['is_attributed'] == 1]
    dloads_os.drop('is_attributed', axis=1, inplace=True)
    
    dloads_channel = df.groupby(['channel','is_attributed'])['os'].count().reset_index()
    dloads_channel.columns = ['channel','is_attributed','dloads_channel']
    dloads_channel = dloads_channel[dloads_channel['is_attributed'] == 1]
    dloads_channel.drop('is_attributed', axis=1, inplace=True)
    
    dloads_app = df.groupby(['app','is_attributed'])['channel'].count().reset_index()
    dloads_app.columns = ['app','is_attributed','dloads_app']
    dloads_app = dloads_app[dloads_app['is_attributed'] == 1]
    dloads_app.drop('is_attributed', axis=1, inplace=True)
    
    gc.collect()    
    
    return nu_apps_ip, nu_channels_ip, nu_os_ip, dloads_os, dloads_channel, dloads_app
    
nu_apps_ip, nu_channels_ip, nu_os_ip, dloads_os, dloads_channel, dloads_app = feature_engineering_2(merge)

train = merge[:nrow_train]
del merge
gc.collect()

def merge_features(df):
    df = pd.merge(df, nu_apps_ip, on='ip', how='left', sort=False)
    df['nu_apps_ip'] = df['nu_apps_ip'].astype('uint16')
    
    df = pd.merge(df, nu_channels_ip, on='ip', how='left', sort=False)
    df['nu_channels_ip'] = df['nu_channels_ip'].astype('uint16')
    print("Feature 3 done")
    
    df = pd.merge(df, nu_os_ip, on='ip', how='left', sort=False)
    df['nu_os_ip'] = df['nu_os_ip'].astype('uint16')
    print("Feature 4 done")
    
    df = pd.merge(df, dloads_os, on='os', how='left', sort=False)
    df['dloads_os'].fillna(0, inplace=True)
    df['dloads_os'] = df['dloads_os'].astype('uint16')
    print("Feature 5 done")
    
    df = pd.merge(df, dloads_channel, on='channel', how='left', sort=False)
    df['dloads_channel'].fillna(0, inplace=True)
    df['dloads_channel'] = df['dloads_channel'].astype('uint16')
    print("Feature 6 done")
    
    df = pd.merge(df, dloads_app, on='app', how='left', sort=False)
    df['dloads_app'].fillna(0, inplace=True)
    df['dloads_app'] = df['dloads_app'].astype('uint16')
    print("Feature 7 done")
     
    gc.collect()   
    return df
     
train = merge_features(train)
y = train['is_attributed']
train.drop(['is_attributed','ip'], axis=1, inplace=True)
gc.collect()


x1, x2, y1, y2 = train_test_split(train, y, test_size=0.1, random_state=99)
dtrain = xgb.DMatrix(x1, y1)
dvalid = xgb.DMatrix(x2, y2)
del x1, y1, x2, y2 
gc.collect()
watchlist = [(dtrain, 'train'), (dvalid, 'valid')]

params = {'eta': 0.2,
                  'tree_method': "hist",
                  'grow_policy': "lossguide",
                  'max_leaves': 1400,  
                  'max_depth': 4, 
                  'subsample': 0.75, 
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
model = xgb.train(params, dtrain, 500, watchlist, maximize=True, early_stopping_rounds = 15, verbose_eval=1)

gc.collect()

from xgboost import plot_importance
import matplotlib.pyplot as plt
plot_importance(model)
plt.gcf().savefig('C:/Kaggle/talkingdata/features/fe_2_scores/feature_importance_3_xgb.png')

end_time = time.time()

print("This script takes ", start_time-end_time)


'''
[99]    train-auc:0.97139       valid-auc:0.971143 - with 3 additional features
[318]   train-auc:0.975348      valid-auc:0.973798 - 3 additional removed
'''

### preds on test
click_time = pd.read_csv(path+"test.csv", usecols=['click_time'])

sub = pd.DataFrame()
sub['click_id'] = test['click_id'].astype('int')
test.drop(['click_id'], axis=1, inplace=True)
gc.collect()

test = merge_features(test)
test.drop('ip', axis=1, inplace=True)
test = timeFeatures(test)
test = test[['app', 'channel', 'device', 'os', 'wday', 'hour', 'nu_apps_ip', 'nu_channels_ip', 'nu_os_ip', 'dloads_os', 'dloads_channel', 'dloads_app']]
dtest = xgb.DMatrix(test)
del train
del dtrain
del dvalid
gc.collect()
y_pred = model.predict(dtest, ntree_limit=model.best_ntree_limit)
sub['is_attributed'] = np.round(y_pred,4)
sub.to_csv('xgb_30m_fe_2_new.csv', index=False)


