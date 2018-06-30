rm(list=ls())
setwd("C:/Users/CGokhale/Downloads/Kaggle/BNP Paribas/Data/")
set.seed(77)

library(plyr)
library(xgboost)
library(Metrics)

train<-read.csv("train.csv",header=T, sep = "|")
test<-read.csv("test.csv",header=T, sep = "|")

for (i in 1:ncol(train)){
  if (is.numeric(train[, i])) train[, i][is.na(train[, i])] <- median(train[,i], na.rm = TRUE)
}

for (i in 1:ncol(test)){
  if (is.numeric(test[, i])) test[, i][is.na(test[, i])] <- median(test[,i], na.rm = TRUE)
}

names(train)
feature.names <- names(train)[-c(1,2)]

for (m in feature.names){
  if (class(train[[m]])=="character"){
    train[[m]] <- as.factor(train[[m]])
    test[[m]] <- as.factor(test[[m]])
  }
}

for (f in feature.names) {
  if (class(train[[f]])=="factor") {
    train[[f]] <- as.numeric(train[[f]])
    test[[f]] <- as.numeric(test[[f]])
  }
}

tra<-train[,feature.names]

h<-sample(nrow(train),round(nrow(train)*0.1))

dval<-xgb.DMatrix(data=data.matrix(tra[h,]),label=train$target[h])
dtrain<-xgb.DMatrix(data=data.matrix(tra[-h,]),label=train$target[-h])
watchlist<-list(val=dval,train=dtrain)
param <- list(  objective           = "reg:linear", 
                booster = "gbtree",
                "eval_metric" = "logloss",
                eta                 = 0.01, # 0.06, #0.01,
                max_depth           = 10, #changed from default of 8
                subsample           = 0.8, # 0.7
                colsample_bytree    = 0.8, # 0.7
                min_child_weight = 1
                #num_parallel_tree   = 2
                # alpha = 0.0001, 
                # lambda = 1
)

clf <- xgb.train(   params              = param, 
                    data                = dtrain, 
                    nrounds             = 540, #300, #280, #125, #250, # changed from 300
                    verbose             = 0,
                    early.stop.round    = 2500,
                    watchlist           = watchlist,
                    maximize            = FALSE,
)

pred <- predict(clf, data.matrix(test[,feature.names]))

submission <- data.frame(Id=test$ID, PredictedProb=pred)
setwd("C:/Users/CGokhale/Downloads/Kaggle/BNP Paribas/Results/")
write.csv(submission,"Simple-xgb-2.csv",row.names=F)
