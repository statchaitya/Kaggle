import gc
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.cross_validation import train_test_split
from sklearn.metrics import roc_auc_score

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
n_clicks_ip = train.groupby(['ip'])['channel'].count().reset_index()
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

train.drop('ip', axis=1, inplace=True)
y = train['is_attributed']
train.drop('is_attributed', axis=1, inplace=True)
xtr, xval, ytr, yval = train_test_split(train, y, test_size=0.1, random_state=99)


gc.collect()
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam
from keras.wrappers.scikit_learn import KerasClassifier

def create_baseline():
    model = Sequential()
    model.add(Dense(10, kernel_initializer='uniform', input_dim=7))
    model.add(Activation('relu'))
    model.add(Dense(5, kernel_initializer='uniform'))
    model.add(Activation('relu'))
    model.add(Dense(1, kernel_initializer='uniform'))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model
 

estimator = KerasClassifier(build_fn=create_baseline, epochs=1, batch_size=10000, verbose=1)
estimator.fit(xtr, ytr)
y_pred_val = estimator.predict_proba(xval)
y_pred_val = pd.DataFrame(y_pred_val)
y_pred_val = y_pred_val.iloc[:,1].values
roc_auc_score(yval, y_pred_val)


del xtr, ytr, xval, yval
gc.collect()
test_columns = train_columns[:-1]
test_columns.append('click_id')
test = pd.read_csv(path+"test.csv", usecols = test_columns, dtype=dtypes)

gc.collect()

sub = pd.DataFrame()
sub['click_id'] = test['click_id'].astype('int')
test.drop(['click_id'], axis=1, inplace=True)
gc.collect()

# creating n_clicks_ip
n_clicks_ip_test = test.groupby(['ip'])['channel'].count().reset_index()
n_clicks_ip_test.columns = ['ip', 'n_clicks_ip']

test = pd.merge(test, n_clicks_ip_test, on='ip', how='left', sort=False)
test['n_clicks_ip'] = test['n_clicks_ip'].astype('uint16')

test = pd.merge(test, app_dloads_yes, on='app', how='left', sort=False)
test['n_clicks_app_1'].fillna(0, inplace=True)
test['n_clicks_app_1'] = test['n_clicks_app_1'].astype('uint16')

test = pd.merge(test, app_dloads_no, on='app', how='left', sort=False)
test['n_clicks_app_0'].fillna(0, inplace=True)
test['n_clicks_app_0'] = test['n_clicks_app_0'].astype('uint16')

test.drop('ip', axis=1, inplace=True)

y_pred = estimator.predict_proba(test)
y_pred = pd.DataFrame(y_pred)
sub['is_attributed'] = np.round(y_pred.iloc[:,1],5)
sub.to_csv('neural_nets_1.csv', index=False)