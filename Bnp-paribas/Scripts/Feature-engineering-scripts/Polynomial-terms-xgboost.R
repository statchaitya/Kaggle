## XGBOOST using Polynomial features ##

rm(list = ls())
set.seed(1234)
setwd('D:/Chaitanya/Kaggle/BNP Paribas/Data/Original')

require(xgboost)

train <- read.csv('train.csv',header=T)
test <- read.csv('test.csv',header=T)

v50tr<- train$v50
v50te<- test$v50

v10tr <- train$v10
v10te<- test$v10

v38tr <- train$v38
v38te <- test$v38

train$v50 <- NULL
train$v38 <- NULL
train$v10 <- NULL

test$v50 <- NULL
test$v38 <- NULL
test$v10 <- NULL

train$v50 <- v50tr^2
train$v38 <- v38tr^2
train$v10 <- v10tr^2

test$v50 <- v50te^2
test$v38 <- v38te^2
test$v10 <- v10te^2

train[is.na(train)] <- -999
test[is.na(test)] <- -999

feature.names <- names(train)[-c(1,2)]

tra<-train[,feature.names]

dtrain<-xgb.DMatrix(data=data.matrix(tra),label=train$target)

param <- list(  objective           = "reg:logistic", 
                booster = "gbtree",
                "eval_metric" = "logloss",
                eta                 = 0.02, # 0.06, #0.01,
                max_depth           = 11, #changed from default of 8
                subsample           = 0.96, # 0.7
                colsample_bytree    = 0.45, # 0.7
                min_child_weight = 1,
                num_parallel_tree   = 1
                # alpha = 0.0001, 
                # lambda = 1
)

clfcv <- xgb.cv(params = param,
                data = dtrain,
                nrounds = 1000,
                nfold = 5,
                prediction = FALSE,
                print.every.n = 20,
                early.stop.round = 50)

