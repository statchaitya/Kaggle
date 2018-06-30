
train$log1pv50 <- log1p(train$v50)
test$log1pv50 <- log1p(test$v50)

train$de.std.log1pv50 <- (sd(train$log1pv50)*train$log1pv50)+ mean(train$log1pv50)
test$de.std.log1pv50 <- (sd(test$log1pv50)*test$log1pv50)+ mean(test$log1pv50)


logmod1 <- glm(target ~ v50, data = train, family = binomial)
pred <- predict(logmod1,test,type= "response")
test$logregv50 <- pred
pred <- predict(logmod1, train, type = "response")
train$logregv50 <- pred


for(i in 1:nrow(train)){
  train[paste("cond.mean.v50")] <- ifelse(train$target[i] == 1 , 1.662053 , 1.1000388)
}

FE_train2..4 <- data.frame(train$ID,train$log1pv50,train$logregv50,train$de.std.log1pv50)
setwd("C:/Users/CGokhale/Downloads/Kaggle/BNP Paribas/Feateng/")
write.csv(FE_train2..4, "feateng2..4-train.csv", row.names = F)

FE_test2..4 <- data.frame(ID = test$ID,log1pv50 = test$log1pv50, logregv50 = test$logregv50,de.std.log1pv50 = test$de.std.log1pv50)
setwd("C:/Users/CGokhale/Downloads/Kaggle/BNP Paribas/Feateng/")
write.csv(FE_test2..4, "feateng2..4-test.csv", row.names = F)

