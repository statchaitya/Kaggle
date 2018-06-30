## XGBOOST using Polynomial features ##

rm(list = ls())
set.seed(1234)
setwd('D:/Chaitanya/Kaggle/BNP Paribas/Data/Original')

require(xgboost)

train <- read.csv('train.csv',header=T)
test <- read.csv('test.csv',header=T)

tremove = c('v8','v23','v25','v31','v36','v37','v46','v51','v53','v54','v63','v73','v75','v79','v81','v82','v89','v92','v95','v105','v107','v108','v109','v110','v116','v117','v118','v119','v123','v124','v128')

train = train[!names(train) %in% tremove]
test <- test[!names(test) %in% tremove]

train1 <- train[,c(11,13,15,22,32,36,45,92)]
test1 <- test[,c(10,12,14,21,31,35,44,91)]

for (i in 1:ncol(train1)){
  if (is.numeric(train1[, i])) train1[, i][is.na(train1[, i])] <- median(train1[,i], na.rm = TRUE)
}

for (i in 1:ncol(test1)){
  if (is.numeric(test1[, i])) test1[, i][is.na(test1[, i])] <- median(test1[,i], na.rm = TRUE)
}


for (i in 1:ncol(train1)){
  train1[paste("Po",2,i,sep = "_")] <- train1[,i]^2
}

for (i in 1:ncol(test1)){
  test1[paste("Po",2,i,sep = "_")] <- test1[,i]^2
}

for (i in 1:8){
  train1[paste("Po",3,i,sep = "_")] <- train1[,i]^3
}

for (i in 1:8){
  test1[paste("Po",3,i,sep = "_")] <- test1[,i]^3
}

for (i in 1:8){
  train1[paste("Po",4,i,sep = "_")] <- train1[,i]^4
}

for (i in 1:8){
  test1[paste("Po",4,i,sep = "_")] <- test1[,i]^4
}

for (i in 1:8){
  train1[paste("Po",5,i,sep = "_")] <- train1[,i]^5
}

for (i in 1:8){
  test1[paste("Po",5,i,sep = "_")] <- test1[,i]^5
}

for (i in 1:8){
  train1[paste("Po",6,i,sep = "_")] <- train1[,i]^6
}

for (i in 1:8){
  test1[paste("Po",6,i,sep = "_")] <- test1[,i]^6
}

for (i in 1:8){
  train1[paste("Po",7,i,sep = "_")] <- train1[,i]^7
}

for (i in 1:8){
  test1[paste("Po",7,i,sep = "_")] <- test1[,i]^7
}

train1 <- train1[,-c(1:8)]
test1 <- test1[-c(1:8)]

trainmain <- cbind(train,train1)
testmain <- cbind(test,test1)

rm(train,test,train1,test1)

train <- trainmain
test <- testmain

rm(trainmain,testmain)

