# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 23:43:51 2018

@author: cgokh
"""

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

train_rows = 184903890
model_train_rows = 30000000
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
del nu_apps_ip, nu_devices_ip, nu_channels_ip, nu_os_ip, nu_wday_ip, nu_hour_ip
y = train['is_attributed']
train.drop(['is_attributed','ip'], axis=1, inplace=True)
gc.collect()


x1, x2, y1, y2 = train_test_split(train, y, test_size=0.1, random_state=99)
dtrain = xgb.DMatrix(x1, y1)
dvalid = xgb.DMatrix(x2, y2)
del x1, y1, x2, y2 
gc.collect()
watchlist = [(dtrain, 'train'), (dvalid, 'valid')]

params = {'eta': 0.1,
                  'tree_method': "hist",
                  'grow_policy': "lossguide",
                  'max_leaves': 1400,  
                  'max_depth': 4, 
                  'subsample': 0.75, 
                  'colsample_bytree': 0.7, 
                  'colsample_bylevel':0.7,
                  'min_child_weight':0.2,
                  'alpha':4,
                  'objective': 'binary:logistic', 
                  'scale_pos_weight':9,
                  'eval_metric': 'auc', 
                  'nthread':8,
                  'random_state': 99, 
                  'silent': True}
model = xgb.train(params, dtrain, 804, watchlist, maximize=True, early_stopping_rounds = 15, verbose_eval=1)
                

gc.collect()

###############################################################################


eta_grid = [0.2,0.1,0.05,0.02]

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
                  'max_depth': 4, 
                  'subsample': 0.8, 
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
        model = xgb.train(params, dtrain, 2500, watchlist, maximize=True, early_stopping_rounds = 15, verbose_eval=1)
                
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
        model = xgb.train(params, dtrain, 1500, watchlist, maximize=True, early_stopping_rounds = 15, verbose_eval=1)
                
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
        model = xgb.train(params, dtrain, 1500, watchlist, maximize=True, early_stopping_rounds = 15, verbose_eval=1)
                
        best_iteration.append(model.best_iteration)
        best_score.append(model.best_score)
        
        del model
        gc.collect()
    
    minchildwt_tuned['best_iteration'] = best_iteration
    minchildwt_tuned['best_score']= best_score
    
    return minchildwt_tuned
        
        
minchildwt_tuned = tune_minchildwt(min_child_wt_grid)
minchildwt_tuned.to_csv('minchildwt_tuned.csv',index=False)



###############################################################################
                
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
test.drop('is_attributed', axis=1, inplace=True)
dtest = xgb.DMatrix(test)
y_pred = model.predict(dtest, ntree_limit=model.best_ntree_limit)
sub['is_attributed'] = np.round(y_pred,4)
sub.to_csv('xgb_30m_fe_2.csv', index=False)