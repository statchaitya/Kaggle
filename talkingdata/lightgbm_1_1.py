

import gc
import pandas as pd
#import numpy as np
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
train_columns = ['ip', 'app', 'device', 'os', 'channel', 'is_attributed']

print("Reading train data")
train = pd.read_csv(path+"train.csv",  skiprows = range(1,skip+1), usecols=train_columns, dtype=dtypes)
print("train data read. train data shape is", train.shape)

gc.collect()

# creating n_clicks_ip
n_clicks_ip = merge.groupby(['ip'])['channel'].count().reset_index()
n_clicks_ip.columns = ['ip', 'n_clicks_ip']
train = pd.merge(train, n_clicks_ip, on='ip', how='left', sort=False)
train['n_clicks_ip'] = train['n_clicks_ip'].astype('uint16')
print("First 10 values of new features are", train['n_clicks_ip'].head())

gc.collect()

# creating n_clicks_app_1
app_count = train.groupby(['app','is_attributed']).count()['ip'].reset_index()
app_count.columns = ['app','is_attributed','n_clicks_app_1']
app_dloads_yes = app_count[app_count['is_attributed'] == 1]
app_dloads_yes.drop('is_attributed', axis=1, inplace=True)

train = pd.merge(train, app_dloads_yes, on='app', how='left', sort=False)
train['n_clicks_app_1'].fillna(0, inplace=True)
train['n_clicks_app_1'] = train['n_clicks_app_1'].astype('uint16')

app_dloads_no = app_count[app_count['is_attributed'] == 0]
app_dloads_no.columns = ['app', 'is_attributed', 'n_clicks_app_0']
app_dloads_no.drop('is_attributed', axis=1, inplace=True)

train = pd.merge(train, app_dloads_no, on='app', how='left', sort=False)
train['n_clicks_app_0'].fillna(0, inplace=True)
train['n_clicks_app_0'] = train['n_clicks_app_0'].astype('uint16')

gc.collect()

y = train['is_attributed']
train.drop('is_attributed', axis=1, inplace=True)
xtr, xval, ytr, yval = train_test_split(train, y, test_size=0.1, random_state=99)

params = {
    'boosting_type': 'gbdt',
    'objective': 'binary',
    'learning_rate': 0.1,
    'metric': 'auc',
    'num_leaves': 7,
    'max_depth': 3,
    'bagging_fraction': 0.85,
    'bagging_freq': 1,
    'feature_fraction': 0.8
}

lgb_train = lgb.Dataset(xtr, ytr)
lgb_eval = lgb.Dataset(xval, yval)

print("Model training")
gbm = lgb.train(params,
                lgb_train,
                num_boost_round=500,
                early_stopping_rounds = 15,
                valid_sets=lgb_eval,
                verbose_eval=True)