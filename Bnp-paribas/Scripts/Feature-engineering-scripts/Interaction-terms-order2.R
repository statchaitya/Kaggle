rm(list=ls())
setwd("D:/Chaitanya/Kaggle/BNP Paribas/Data/original/")
set.seed(77)

train<-read.csv("train.csv",header=T)
test<-read.csv("test.csv",header=T)

d <-(combn(20,2,simplify = TRUE))

d1<-as.data.frame(d)

v1<-d1[1,]
v2<-d1[2,]

v1<-c(v1)
v2<-c(v2)

v1 <- as.numeric(v1)
v2 <- as.numeric(v2)

## Now try to loop the values of v1 and v2
require(dplyr)
train <- train[names(train) %in% c('v50','v66','v12','v24','v114','v34','v40','v112','v21','v47','v56','v52','v14','v22','v10','v62','v113','v129','v125','v6')]
test <- test[names(test) %in% c('v50','v66','v12','v24','v114','v34','v40','v112','v21','v47','v56','v52','v14','v22','v10','v62','v113','v129','v125','v6')]

for (i in 1:ncol(train)){
  if (is.numeric(train[, i])) train[, i][is.na(train[, i])] <- median(train[,i], na.rm = TRUE)
}

for (i in 1:ncol(test)){
  if (is.numeric(test[, i])) test[, i][is.na(test[, i])] <- median(test[,i], na.rm = TRUE)
}

for (i in 1:20){
  if( is.factor(train[,i])) train[,i] <- as.numeric(train[,i])
}

for (i in 1:20){
  if( is.factor(test[,i])) test[,i] <- as.numeric(test[,i])
}


i = 1
for (j in i+1:19) {
  train[paste('v_1',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_1',j,sep = "+" )] <- test[,i]*test[,j]
}

i = 2
for (j in i+1:18) {
  train[paste('v_2',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_2',j,sep = "+" )] <- test[,i]*test[,j]
}

i = 3
for (j in i+1:17) {
  train[paste('v_3',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_3',j,sep = "+" )] <- test[,i]*test[,j]
}

i = 4
for (j in i+1:16) {
  train[paste('v_4',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_4',j,sep = "+" )] <- test[,i]*test[,j]
}

i = 5
for (j in i+1:15) {
  train[paste('v_5',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_5',j,sep = "+" )] <- test[,i]*test[,j]
}

i = 6
for (j in i+1:14) {
  train[paste('v_6',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_6',j,sep = "+" )] <- test[,i]*test[,j]
}

i = 7
for (j in i+1:13) {
  train[paste('v_7',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_7',j,sep = "+" )] <- test[,i]*test[,j]
}

i = 8
for (j in i+1:12) {
  train[paste('v_8',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_8',j,sep = "+" )] <- test[,i]*test[,j]
}

i = 9
for (j in i+1:11) {
  train[paste('v_9',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_9',j,sep = "+" )] <- test[,i]*test[,j]
}

i = 10
for (j in i+1:10) {
  train[paste('v_10',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_10',j,sep = "+" )] <- test[,i]*test[,j]
}

i = 11
for (j in i+1:9) {
  train[paste('v_11',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_11',j,sep = "+" )] <- test[,i]*test[,j]
}

i = 12
for (j in i+1:8) {
  train[paste('v_12',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_12',j,sep = "+" )] <- test[,i]*test[,j]
}

i = 13
for (j in i+1:7) {
  train[paste('v_13',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_13',j,sep = "+" )] <- test[,i]*test[,j]
}

i = 14
for (j in i+1:6) {
  train[paste('v_14',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_14',j,sep = "+" )] <- test[,i]*test[,j]
}

i = 15
for (j in i+1:5) {
  train[paste('v_15',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_15',j,sep = "+" )] <- test[,i]*test[,j]
}

i = 16
for (j in i+1:4) {
  train[paste('v_16',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_16',j,sep = "+" )] <- test[,i]*test[,j]
}

i = 17
for (j in i+1:3) {
  train[paste('v_17',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_17',j,sep = "+" )] <- test[,i]*test[,j]
}

i = 18
for (j in i+1:2) {
  train[paste('v_18',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_18',j,sep = "+" )] <- test[,i]*test[,j]
}

i = 19
for (j in i+1:1) {
  train[paste('v_19',j,sep = "+" )] <- train[,i]*train[,j]
  test[paste('v_19',j,sep = "+" )] <- test[,i]*test[,j]
}

setwd("D:/Chaitanya/Kaggle/BNP Paribas/Data/Eng feat/Eng1/")


# Keeping 1 column v6 so that merging to original train and test is easy

train <- train[,-c(2:20)]
test <- test[,-c(2:20)]

