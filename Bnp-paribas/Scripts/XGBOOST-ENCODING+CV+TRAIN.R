rm(list=ls())
setwd("C:/Users/CGokhale/Downloads/Kaggle/BNP Paribas/Data/")
set.seed(77)

library(plyr)
library(xgboost)
library(Metrics)

train<-read.csv("train.csv",header=T, sep = "|")
test<-read.csv("test.csv",header=T)

for (i in 1:ncol(train)){
  if (is.numeric(train[, i])) train[, i][is.na(train[, i])] <- median(train[,i], na.rm = TRUE)
}

for (i in 1:ncol(test)){
  if (is.numeric(test[, i])) test[, i][is.na(test[, i])] <- median(test[,i], na.rm = TRUE)
}

## Taking all the indexes of categorical vars in f

f <- c()
for (i in 1:ncol(train)){
  if (is.factor(train[, i])) f <- c(f,i)
}

f #Has all the indexes of all categorical variables

#g <- c() #USe if you want to use a subset of categorical vars for one hot encoding having at most x=26 categories.
#for (i in f){
#  if (length(levels(train[,i])) <= 26 ) g <-c(g,i)
#}

g <- c()
g <- f

g #Has all the indexes of all categorical vars in the data having at most 5 categories OR ALL CATEGORIES depending upon the syntax before this

dum <- g
dummyframe <- train[,dum]

# Main loop used for dummying. Dummied vars will be saved in dummyframe itself

for(i in 1:ncol(dummyframe)){
  if(is.factor(dummyframe[,i]) == TRUE){
    for(level in unique(dummyframe[,i])){
      dummyframe[paste("dummy", level , i , sep = "_")] <- ifelse(dummyframe[,i] == level,1,0)
    }
  }  
}

# Removing the original vars from dummyframe and naming the train dummy frame to
# 'dummyframe1'


temp <- 1:length(g)
dummyframe1 <- dummyframe[,-temp]

rm(dummyframe)

## For test
# Converting all the integer vars to factors

for(i in ncol(test)){
  if(is.integer(test[,i]) == TRUE){
    test[,i] = as.factor(test[,i])
  }  
}

h <- c()
for (i in 1:ncol(test)){
  if (is.factor(test[, i])) h <- c(h,i)
}

#j <- c()  #Use this incase you want to use a subset of categorical vars for one hot encoding
#for (i in h){
#  if (length(levels(test[,i])) <= 26 ) j <-c(j,i)
#}

j <- c()
j <- h

# taking out the indexes of all those factor vars to be dummied
# and separating those columns in an independent df name 'dummyframe'

dum <- j
dummyframe <- test[,dum]

# Main loop used for dummying. Dummied vars will be saved in dummyframe itself

for (i in ncol(dummyframe)){
  dummyframe[,i] <- as.factor(dummyframe[,i])
}

for(i in 1:ncol(dummyframe)){
  if(is.factor(dummyframe[,i]) == TRUE){
    for(level in unique(dummyframe[,i])){
      dummyframe[paste("dummy", level , i , sep = "_")] <- ifelse(dummyframe[,i] == level,1,0)
    }
  }  
}

# Removing the original vars. naming the test dummy vars as 'dummyframe2'

temp <- 1:length(j)
dummyframe2 <- dummyframe[,-temp]

# Keeping only the common columns in both the TRAIN AND TEST dummyframes
# i.e. dummyframe1 and dummyframe2

# Use only when one of the category in 1 variable in absent in the other data set

#negnames <- c()

#for (i in 1:ncol(dummyframe1)){
 # if (!(colnames(dummyframe1[i]) %in% colnames(dummyframe2))){
  #  negnames <- append(negnames,colnames(dummyframe1[i]))
  #}
#}

#dummyframe1 <- dummyframe1[ , -which(names(dummyframe1) %in% negnames)]
 
# Again repeating the same procudure because it was necessary in this case
# due to unknown reason

#negnames1<- c()

#for (i in 1:ncol(dummyframe2)){
 # if (!(colnames(dummyframe2[i]) %in% colnames(dummyframe1))){
  #  negnames1 <- append(negnames1,colnames(dummyframe2[i]))
  #}
#}

#dummyframe2 <- dummyframe2[ , -which(names(dummyframe2) %in% negnames1)]

# Combining the dummies with the data


train <- train[,-g]
test <- test[,-j]

train <- data.frame(train,dummyframe1)
test <- data.frame(test,dummyframe2)

# Remvoing dummyframes used for manupilation

rm(dummyframe,dummyframe1,dummyframe2)

#####################

## MAIN XGBOOST ##

#####################



setwd("C:/Users/CGokhale/Downloads/Kaggle/BNP Paribas/Feateng/")

trainfeat1<- read.csv("FE1-train.csv",header= T, sep = "|")
testfeat1<- read.csv("FE1-test.csv", header= T)

train <- merge(train,trainfeat1, by= "ID")
test <- merge(test,testfeat1, by = "ID")


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

dtrain<-xgb.DMatrix(data=data.matrix(tra),label=train$target)

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

clfcv <- xgb.cv(params = param,
                 data = dtrain,
                 nrounds = 1600,
                 nfold = 5,
                 prediction = FALSE,
                 print.every.n = 20,
                 early.stop.round = 50)

clf <- xgb.train(   params              = param, 
                    data                = dtrain, 
                    nrounds             = 1000, #300, #280, #125, #250, # changed from 300
                    verbose             = 0,
                    maximize            = FALSE,
)

pred <- predict(clf, data.matrix(test[,feature.names]))

submission <- data.frame(Id=test$ID, PredictedProb=pred)
setwd("C:/Users/CGokhale/Downloads/Kaggle/BNP Paribas/Results/")
write.csv(submission,"xgb-one-hot-encoding-all-categorical.csv",row.names=F)
