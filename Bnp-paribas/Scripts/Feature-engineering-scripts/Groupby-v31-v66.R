
#### LOAD TRAIN AND TEST DATA FIRST !!!!


d1 <- filter(train, train$v66 %in% c("C"))
d11 <- filter (d1, d1$v31 %in% c("C"))
m12 <- mean(d11$target)
rm(d1,d11)

m <- c(m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12)


#--------------------------

df <- data.frame(ID = train[,1], target = train[,2], v31 = train[,33], v66 = train[,68])

L31 <- levels(df$v31)
L66 <- levels(df$v66)


d <- filter(df, df$v31 %in% c(""))
d6611 <- filter(d , d$v66 %in% c("A"))
d6612 <- filter(d, d$v66 %in% c("B"))
d6613 <- filter(d, d$v66 %in% c("C"))
rm(d)
d <-filter(df, df$v31 %in% c("A"))
d6621 <- filter(d, d$v66 %in% c("A"))
d6622 <- filter(d, d$v66 %in% c("B"))
d6623 <- filter(d, d$v66 %in% c("C"))
rm(d)
d<- filter(df, df$v31 %in% c("B"))
d6631 <- filter(d, d$v66 %in% c("A"))
d6632 <- filter(d, d$v66 %in% c("B"))
d6633 <- filter(d, d$v66 %in% c("C"))
rm(d)
d <- filter(df , df$v31 %in% c("C"))
d6641 <- filter(d, d$v66 %in% c("A"))
d6642 <- filter(d, d$v66 %in% c("B"))
d6643 <- filter(d, d$v66 %in% c("C"))
rm(d)

d6611[paste("gb.31.66.mean")] <- m1
d6612[paste("gb.31.66.mean")] <- m2
d6613[paste("gb.31.66.mean")] <- m3

d6621[paste("gb.31.66.mean")] <- m4
d6622[paste("gb.31.66.mean")] <- m5
d6623[paste("gb.31.66.mean")] <- m6

d6631[paste("gb.31.66.mean")] <- m7
d6632[paste("gb.31.66.mean")] <- m8
d6633[paste("gb.31.66.mean")] <- m9

d6641[paste("gb.31.66.mean")] <- m10
d6642[paste("gb.31.66.mean")] <- m11
d6643[paste("gb.31.66.mean")] <- m12

fe5tr <- rbind(d6611,d6612,d6613,d6621,d6622,d6623,d6631,d6632,d6633,d6641,d6643)

train <- merge(train,fe5tr, by = c("ID"))

train$v66.y <- NULL
train$v31.y <- NULL
train$target.y <- NULL

names(train)[names(train) == "target.x"] <- "target"
names(train)[names(train) == "v31.x"] <- "v31"
names(train)[names(train) == "v66.x"] <- "v66"

names(train)

########################
### --- FOR TEST --- ###
########################

rm(df,d,d6611,d6612,d6613,d6621,d6622,d6623,d6631,d6632,d6633,d6641,d6642,d6643)

df <- data.frame(ID = test[,1], v31 = test[,32], v66 = test[,67])

d <- filter(df, df$v31 %in% c(""))
d6611 <- filter(d , d$v66 %in% c("A"))
d6612 <- filter(d, d$v66 %in% c("B"))
d6613 <- filter(d, d$v66 %in% c("C"))
rm(d)
d <-filter(df, df$v31 %in% c("A"))
d6621 <- filter(d, d$v66 %in% c("A"))
d6622 <- filter(d, d$v66 %in% c("B"))
d6623 <- filter(d, d$v66 %in% c("C"))
rm(d)
d<- filter(df, df$v31 %in% c("B"))
d6631 <- filter(d, d$v66 %in% c("A"))
d6632 <- filter(d, d$v66 %in% c("B"))
d6633 <- filter(d, d$v66 %in% c("C"))
rm(d)
d <- filter(df , df$v31 %in% c("C"))
d6641 <- filter(d, d$v66 %in% c("A"))
d6642 <- filter(d, d$v66 %in% c("B"))
d6643 <- filter(d, d$v66 %in% c("C"))
rm(d)

d6611[paste("gb.31.66.mean")] <- m1
d6612[paste("gb.31.66.mean")] <- m2
d6613[paste("gb.31.66.mean")] <- m3

d6621[paste("gb.31.66.mean")] <- m4
d6622[paste("gb.31.66.mean")] <- m5
d6623[paste("gb.31.66.mean")] <- m6

d6631[paste("gb.31.66.mean")] <- m7
d6632[paste("gb.31.66.mean")] <- m8
d6633[paste("gb.31.66.mean")] <- m9

d6641[paste("gb.31.66.mean")] <- m10
d6642[paste("gb.31.66.mean")] <- m11
d6643[paste("gb.31.66.mean")] <- m12

fe5te <- rbind(d6611,d6612,d6613,d6621,d6622,d6623,d6631,d6632,d6633,d6641,d6643)

test <- merge(test,fe5te, by = c("ID"))

test$v66.y <- NULL
test$v31.y <- NULL

names(test)[names(test) == "v31.x"] <- "v31"
names(test)[names(test) == "v66.x"] <- "v66"

setwd("D:\\Chaitanya\\Kaggle\\BNP Paribas\\Data\\")
write.csv(train, "train-gb.mean.66.31.csv", row.names = F)
write.csv(test, "test-gb.mean.66.31.csv", row.names = F)
