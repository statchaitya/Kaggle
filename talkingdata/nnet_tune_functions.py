
import gc
from sklearn.cross_validation import train_test_split
from sklearn.metrics import roc_auc_score
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
 
xtr, xval, ytr, yval = train_test_split(train, y, test_size=0.1, random_state=99)
del train, y

def tune_epochs(estimator, epoch_num, train, y):
	gc.collect()
	epoch_list = range(1:epoch_num+1)
	epoch_val_score = pd.DataFrame()
	epoch_val_score['epochs'] = epoch_list
	epoch_scores = []
	for epoch in epoch_list:
		estimator = KerasClassifier(build_fn=create_baseline, epochs=epoch, batch_size=5000, verbose=1)
		estimator.fit(xtr, ytr)
		y_pred_val = estimator.predict_proba(xval)
		del estimator
		gc.collect()
		y_pred_val = pd.DataFrame(y_pred_val)
		y_pred_val = y_pred_val.iloc[:,1].values
		epoch_scores.append(roc_auc_score)
		del y_pred_val
		
	epoch_val_score['val_scores'] = epoch_scores
	
	return epoch_val_score