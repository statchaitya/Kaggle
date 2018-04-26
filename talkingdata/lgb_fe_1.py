# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 20:18:23 2018

@author: cgokh
"""


import gc
import pandas as pd
import numpy as np
import lightgbm as lgb
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

train_rows = 184903890
model_train_rows = 50000000
skip = train_rows - model_train_rows
train_columns = ['ip', 'app', 'device', 'os', 'channel', 'click_time','is_attributed']

train = pd.read_csv(path+"train.csv",  skiprows = range(1,skip+1), dtype=dtypes)
print("train data read. train data shape is", train.shape)


print("Starting feature engineering")
def feature_engineering(df):
    df['datetime'] = pd.to_datetime(df['click_time'])
    df['wday'] = df['datetime'].dt.dayofweek
    df["hour"] = df["datetime"].dt.hour
    df.drop(['click_time', 'datetime'], axis=1, inplace=True)
    
    most_freq_hours_in_test_data = [4,5,9,10,13,14]
    least_freq_hours_in_test_data = [6,11,15]
    
    df['in_test_hh'] = np.where(df['hour'].isin(most_freq_hours_in_test_data), 1, np.where(df['hour'].isin(least_freq_hours_in_test_data), 3, 2))
    print("Feature 1 done")
    # Number of clicks for a particular IP,DAY,DIFFERENT TIMES OF DAY
    nip_day_test_hh = df.groupby(['ip','wday','in_test_hh'])['channel'].count().reset_index()
    nip_day_test_hh.columns = ['ip', 'wday','in_test_hh', 'nip_day_test_hh']
    df = pd.merge(df, nip_day_test_hh, on=['ip','wday','in_test_hh'], how='left', sort=False)
    df['nip_day_test_hh'] = df['nip_day_test_hh'].astype('uint16')
    del nip_day_test_hh
    print("Feature 2 done")
    df.drop(['in_test_hh'], axis=1, inplace=True)
    
    nip = df.groupby(['ip','wday','hour'])['channel'].count().reset_index()
    nip.columns = ['ip', 'wday','hour', 'nip']
    df = pd.merge(df, nip, on=['ip','wday','hour'], how='left', sort=False)
    df['nip'] = df['nip'].astype('uint16')
    del nip
    print("Feature 3 done")
    gc.collect()
    
    nip = df.groupby(['ip','wday','hour','os'])['channel'].count().reset_index()
    nip.columns = ['ip', 'wday','hour','os', 'nip_os']
    df = pd.merge(df, nip, on=['ip','wday','hour','os'], how='left', sort=False)
    df['nip_os'] = df['nip_os'].astype('uint16')
    del nip
    
    gc.collect()
    print("Feature 4 done")
    nip = df.groupby(['ip','wday','hour','app'])['channel'].count().reset_index()
    nip.columns = ['ip', 'wday','hour','app', 'nip_app']
    df = pd.merge(df, nip, on=['ip','wday','hour','app'], how='left', sort=False)
    df['nip_app'] = df['nip_app'].astype('uint16')
    del nip
    
    gc.collect()    
    
    nip = df.groupby(['ip','wday','hour','app','os'])['channel'].count().reset_index()
    nip.columns = ['ip', 'wday','hour','app','os', 'nip_app_os']
    df = pd.merge(df, nip, on=['ip','wday','hour','app','os'], how='left', sort=False)
    df['nip_app_os'] = df['nip_app_os'].astype('uint16')
    del nip
    
    gc.collect()    
    
    nip = df.groupby(['app','wday','hour'])['channel'].count().reset_index()
    nip.columns = ['app','wday','hour','n_app']
    df = pd.merge(df, nip, on=['app','wday','hour'], how='left', sort=False)
    df['n_app'] = df['n_app'].astype('uint16')
    del nip
    print("Creating last feature")
    app_dloads_yes = pd.read_csv('C:/Kaggle/talkingdata/features/app_dloads_yes.csv')
    app_dloads_yes['app_dloads_log1p'] = np.log1p(app_dloads_yes['clicks_app_is_atr_1'])
    app_dloads_yes.drop('clicks_app_is_atr_1', axis=1, inplace=True)
    df = pd.merge(df, app_dloads_yes, on='app', how='left', sort=False)
    
    gc.collect()    
    
    return df
	

train = feature_engineering(train)
gc.collect()

y = train['is_attributed']
train.drop(['is_attributed','ip','wday', 'attributed_time'], axis=1, inplace=True)
xtr, xval, ytr, yval = train_test_split(train, y, test_size=0.1, random_state=99)
del train, y

params = {
    'boosting_type': 'gbdt',
    'objective': 'binary',
    'learning_rate': 0.1,
    'metric': 'auc',
    'num_leaves': 7,
    'max_depth': 4,
    'min_data_in_leaf': 100,
    'bagging_fraction': 0.7,
    'bagging_freq': 1,
    'feature_fraction': 0.7,
    'min_sum_hessian_in_leaf': 0,
    'scale_pos_weight': 200
}

categorical_vars = ["app", "device", "os", "channel", "hour"]

lgb_train = lgb.Dataset(xtr, ytr)
lgb_eval = lgb.Dataset(xval, yval)
del xtr, ytr, xval, yval

print("Model training")
gbm = lgb.train(params,
                lgb_train,
                num_boost_round=1500,
                early_stopping_rounds = 50,
                categorical_feature = categorical_vars,
                valid_sets=lgb_eval,
                verbose_eval=True)


gc.collect()
test_columns = train_columns[:-1]
test_columns.append('click_id')
test = pd.read_csv(path+"test.csv", usecols = test_columns, dtype=dtypes)

gc.collect()

sub = pd.DataFrame()
sub['click_id'] = test['click_id'].astype('int')
test.drop(['click_id'], axis=1, inplace=True)
gc.collect()

test = feature_engineering(test)

test.drop('ip', axis=1, inplace=True)

y_pred = gbm.predict(test, num_iteration=gbm.best_iteration)
sub['is_attributed'] = np.round(y_pred,4)
sub.to_csv('lightgbm_laptop_1.csv', index=False)
	
'''	
Early stopping, best iteration is:
[938]   valid_0's auc: 0.974955
'''