rm(list=ls())
setwd("C:/Users/CGokhale/Downloads/Kaggle/BNP Paribas/Data/Original/")
set.seed(77)

library(plyr)
require(dplyr)

train<-read.csv("train.csv",header=T, sep = "|")
test<-read.csv("test.csv",header=T, sep = "|")

f <- c()
for (i in 1:52){
  if(is.factor(train[,i])) f <- c(f,i)
}

unique(levels(h$comb5))

g <- c()
for (i in 1:52){
  if(is.factor(test[,i])) g <- c(g,i)
}

f
f <- f[-c(2)]

g
g <- g[-c(2)]

train$v47 = revalue(train$v47, c("H" = "A"))

h <- ddply(train, names(train)[f], function(df)mean(df$target))
h1 <- ddply(test, names(test)[g], function(df)mean(test$v50))

for (i in 1:5){
  levels(h[,i])[levels(h[,i])==""] <- "Blank"
}

for (i in 1:5){
  levels(h1[,i])[levels(h1[,i])==""] <- "Blank"
}

for (i in g){
  levels(test[,i])[levels(test[,i])==""] <- "Blank"
}

h$comb5 <- paste(h[,1],h[,2],h[,3],h[,4],h[,5], sep = ".")
h1$comb5 <- paste(h1[,1],h1[,2],h1[,3],h1[,4],h1[,5], sep = ".")
test$comb5 <- paste(test[,4],test[,25],test[,31],test[,32],test[,48], sep =".")

h3 <- h[,c(6,7)]
h4 <- data.frame(h1[,c(7)])
colnames(h4) <- c("comb5")

h5 <- merge(h3,h4, by = c("comb5"), all.x = TRUE)

rm(h,h1,h3,h4)

test1 <- filter(test, test$comb5 %in% levels(h$comb5))
test2 <- filter(test, !(test$comb5 %in% levels(h$comb5)))

test2$group1.tar.mean <- ifelse( test2$v50 >= 1.4, 0.99, 0.25 )

d <- list()
r <- list()

for (i in 1:nrow(h5)){
  d[[i]] <- data.frame()
  d[[i]] <- filter(test1, test1$comb5 %in% h5$comb5[i])
  r[[i]] <- data.frame(ID = d[[i]]$ID, group1.tar.mean = rep(0,nrow(d[[i]])))
  r[[i]]$group1.tar.mean = rep(h5$V1[i], nrow(d[[i]]))
  cat(i,"\n")
}

rr1 <- do.call("rbind",r)
rr2 <- data.frame(ID = test2$ID, group1.tar.mean = test2$group1.tar.mean)

rmain = rbind(rr1,rr2)

test<- merge(test,rmain, by = c("ID"))

rm(test1,test2,rr1,rr2,r,rmain,d,h,h1,h3,h4,h5)

test$comb5 <- NULL

### - Main feature engineering - ###


for (i in 1:ncol(train)){
  if (is.numeric(train[, i])) train[, i][is.na(train[, i])] <- median(train[,i], na.rm = TRUE)
}

for (i in 1:ncol(test)){
  if (is.numeric(test[, i])) test[, i][is.na(test[, i])] <- median(test[,i], na.rm = TRUE)
}

train$group1.tar.mean <- ave(train$target, train[,5], train[,26],train[,32], train[,33],train[,49], FUN=mean)

train$group1.v50.mean <- ave(train$v50, train[,5], train[,26],train[,32], train[,33],train[,49], FUN=mean)

f1 <- c(12,14,16,23,36,42,52,116)
g1 <- c(11,13,15,22,35,41,51,115)

f1 <- names(train)[f1]
g1 <- names(test)[g1]

for (i in f1){
  train[paste('group1',i,'mean', sep = ".")] <- ave(train[,i], train[,5], train[,26],train[,32], train[,33],train[,49], FUN=mean)
}

for (i in g1){
  test[paste('group1',i,'mean', sep = ".")] <- ave(test[,i], test[,4], test[,25],train[,32], test[,32],test[,48], FUN=mean)
}

for (i in names(train)[135:142]){
  train[paste(i,'^2',sep = "_")] <- train[,i]^2
}

for (i in names(test)[134:141]){
  test[paste(i,'^2',sep = "_")] <- test[,i]^2
}


for (k in 3:10)
  {
for (i in names(train)[135:142]){
  train[paste(i,'^',k,sep = "_")] <- train[,i]^k
}

for (i in names(test)[134:141]){
  test[paste(i,'^',k,sep = "_")] <- test[,i]^k
}
}

for (i in names(train)[135:214]){
  train[paste(i,'prob','mult',sep = "_")] <- train[,i]*train$group1.tar.mean 
}

for (i in names(test)[134:213]){
  test[paste(i,'prob','mult',sep = "_")] <- test[,i]*test$group1.tar.mean
}

setwd("C:/Users/CGokhale/Downloads/Kaggle/BNP Paribas/Data/")

write.csv(train,'train-group1-prob-mult.csv', row.names = F)
write.csv(test,'test-group1-prob-mult.csv', row.names = F)

trainmain <- train
testmain <- test

train <- train[,c(1,2,134:294)]
test <- test[,c(1,133:293)]

feature.names <- names(train)[-c(1,2)]

tra<-train[,feature.names]

dtrain<-xgb.DMatrix(data=data.matrix(tra),label=train$target)

param <- list(  objective           = "reg:logistic", 
                booster = "gbtree",
                "eval_metric" = "logloss",
                eta                 = 0.02, # 0.06, #0.01,
                max_depth           = 10, #changed from default of 8
                subsample           = 0.7, # 0.7
                colsample_bytree    = 0.5, # 0.7
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
                    nrounds             = 800, #300, #280, #125, #250, # changed from 300
                    verbose             = 0,
                    maximize            = FALSE,
)

pred <- predict(clf, data.matrix(test[,feature.names]))

submission <- data.frame(Id=test$ID, PredictedProb=pred)
setwd("C:/Users/CGokhale/Downloads/Kaggle/BNP Paribas/Results/")
write.csv(submission,"xgb-one-hot-encoding-all-categorical.csv",row.names=F)