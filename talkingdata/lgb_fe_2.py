# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 13:26:41 2018

@author: cgokh
"""

#from sklearn.decomposition import PCA
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
train = pd.read_csv(path+"train.csv",  skiprows = range(1,skip+1), usecols = train_columns, dtype=dtypes)
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
    
    nu_devices_ip = df.groupby(['ip'])['device'].nunique().reset_index()
    nu_devices_ip.columns = ['ip', 'nu_devices_ip']
    #df = pd.merge(df, nu_devices_ip, on='ip', how='left', sort=False)
    #df['nu_devices_ip'] = df['nu_devices_ip'].astype('uint16')
    print("Feature 2 done")
    
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
    
    nu_wday_ip = df.groupby(['ip'])['wday'].nunique().reset_index()
    nu_wday_ip.columns = ['ip', 'nu_wday_ip']
    #df = pd.merge(df, nu_wday_ip, on='ip', how='left', sort=False)
    #df['nu_wday_ip'] = df['nu_wday_ip'].astype('uint16')
    print("Feature 5 done")
    
    nu_hour_ip = df.groupby(['ip'])['hour'].nunique().reset_index()
    nu_hour_ip.columns = ['ip', 'nu_hour_ip']
    #df = pd.merge(df, nu_hour_ip, on='ip', how='left', sort=False)
    #df['nu_hour_ip'] = df['nu_hour_ip'].astype('uint16')
    print("Feature 6 done")
    
    gc.collect()    
    
    return nu_apps_ip, nu_devices_ip, nu_channels_ip, nu_os_ip, nu_wday_ip, nu_hour_ip
	
nu_apps_ip, nu_devices_ip, nu_channels_ip, nu_os_ip, nu_wday_ip, nu_hour_ip = feature_engineering_2(merge)

train = merge[:nrow_train]
del merge
gc.collect()

def merge_features(df):
    df = pd.merge(df, nu_apps_ip, on='ip', how='left', sort=False)
    df['nu_apps_ip'] = df['nu_apps_ip'].astype('uint16')
    
    df = pd.merge(df, nu_devices_ip, on='ip', how='left', sort=False)
    df['nu_devices_ip'] = df['nu_devices_ip'].astype('uint16')
    print("Feature 2 done")

    df = pd.merge(df, nu_channels_ip, on='ip', how='left', sort=False)
    df['nu_channels_ip'] = df['nu_channels_ip'].astype('uint16')
    print("Feature 3 done")
    
    df = pd.merge(df, nu_os_ip, on='ip', how='left', sort=False)
    df['nu_os_ip'] = df['nu_os_ip'].astype('uint16')
    print("Feature 4 done")
    
    df = pd.merge(df, nu_wday_ip, on='ip', how='left', sort=False)
    df['nu_wday_ip'] = df['nu_wday_ip'].astype('uint16')
    print("Feature 5 done")
    
    df = pd.merge(df, nu_hour_ip, on='ip', how='left', sort=False)
    df['nu_hour_ip'] = df['nu_hour_ip'].astype('uint16')
    print("Feature 6 done")
    
    gc.collect()   
    return df
     
train = merge_features(train) 
y = train['is_attributed']
train.drop(['is_attributed','ip'], axis=1, inplace=True)
gc.collect()

xtr, xval, ytr, yval = train_test_split(train, y, test_size=0.1, random_state=99)
del train, y

params = {
    'boosting_type': 'gbdt',
    'objective': 'binary',
    'learning_rate': 0.3,
    'metric': 'auc',
    'num_leaves': 7,
    'max_depth': 3,
    'min_data_in_leaf': 100,
    'bagging_fraction': 0.85,
    'bagging_freq': 1,
    'feature_fraction': 0.7,
    'min_sum_hessian_in_leaf': 0,
    'scale_pos_weight': 200
}

#categorical_vars = ["app", "device", "os", "channel", "hour"]

lgb_train = lgb.Dataset(xtr, ytr)
lgb_eval = lgb.Dataset(xval, yval)
del xtr, ytr, xval, yval
gc.collect()

print("Model training")
gbm = lgb.train(params,
                lgb_train,
                num_boost_round=1500,
                early_stopping_rounds = 25,
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

test = feature_engineering_2(test)

test.drop('ip', axis=1, inplace=True)

y_pred = gbm.predict(test, num_iteration=gbm.best_iteration)
sub['is_attributed'] = np.round(y_pred,4)
sub.to_csv('lightgbm_fe_2.csv', index=False)