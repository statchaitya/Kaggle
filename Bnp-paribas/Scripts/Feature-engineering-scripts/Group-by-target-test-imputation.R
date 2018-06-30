rm(list=ls())
setwd("C:/Users/CGokhale/Downloads/Kaggle/BNP Paribas/Data/Original/")
set.seed(77)

library(plyr)
require(dplyr)
require(stringi)

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


