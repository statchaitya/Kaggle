### THIS CODE WAS ALSO USED FOR V56.

for (i in levels(train$v56)){
  if (i == "") levels(train$v56)[levels(train$v56)==""] <- "A"
}


Letters <- toupper(letters)

for (i in Letters){
  for (j in levels(train$v56)){
    if ((toupper(substr(j,1,1))) == i)  levels(train$v56)[levels(train$v56)==j] <- i
  }
}

for (i in levels(test$v56)){
  if (i == "") levels(test$v56)[levels(test$v56)==""] <- "A"
}


Letters <- toupper(letters)

for (i in Letters){
  for (j in levels(test$v56)){
    if ((toupper(substr(j,1,1))) == i)  levels(test$v56)[levels(test$v56)==j] <- i
  }
}


write.csv(train,"train_FEv56_median.csv",row.names= FALSE)
write.csv(test,"test_FEv56_median.csv",row.names = FALSE)
