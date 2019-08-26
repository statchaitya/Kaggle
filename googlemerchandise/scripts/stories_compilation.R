library(tidyverse)
library(lubridate)
library(reshape2)
library(plotly)

dtrain <- read.csv("C:/Kaggle/googlemerchandise/data/train_new.csv", stringsAsFactors = F)
dtrain$date <- ymd(dtrain$date)
dtrain$transactionRevenue <- as.numeric(dtrain$transactionRevenue)
dtrain$transactionRevenue[is.na(dtrain$transactionRevenue)] <- 0

dtrain$pageviews[is.na(dtrain$pageviews)] <- 0
dtrain$pageviews <- as.numeric(dtrain$pageviews)
dtrain$bounces[is.na(dtrain$bounces)] <- 0
dtrain$bounces <- as.numeric(dtrain$bounces)
dtrain$newVisits[is.na(dtrain$newVisits)] <- 0
dtrain$newVisits <- as.numeric(dtrain$newVisits)

########################## STORY 1 ###############################

# We asked the question which channel has the highest visit level conversion rate?
# Visits coming from referrals had the highest conversion rate followed by display and paid search
# Within visits coming from referrals, the ones coming from NY, Chicago and Ann Arbor had the hiest
# CR with NY pulling the hiest rev among the above mentioned locations. Referrals coming from Japan and
# london had the least CRs.


s1 <- dtrain %>% filter(channelGrouping == "Referral") %>%
  group_by(city, country) %>%
  summarise(totalConversions = sum(transactionRevenueNew > 0),
            totalSessions = n(),
            totalRevenue = sum(transactionRevenueNew)) %>%
  mutate(ConversionRate = (totalConversions/totalSessions)*100) %>%
  filter(totalSessions > 1000) %>%
  arrange(desc(totalRevenue))

s1[15,][["city"]] = "Unknown"
s1 <- s1 %>% mutate(city_country = paste(city, country, sep = ", "))

s1_ggdata <- s1 %>% 
  filter(city %in% c("Unknown", "New York", "Ann Arbor", "Chicago", "London")) %>% 
  ungroup() %>% 
  select(city_country, totalSessions, totalConversions, ConversionRate) %>% 
  mutate(cr_category = if_else(city_country %in% c("Unknown, Japan", "London, United Kingdom"), 
                               "Seldom Convert", 
                               "Frequently Convert")) %>% 
  melt(id = c("city_country", "cr_category"))

theme_set(theme_classic())

ggplot(data = s1_ggdata %>%
         filter(variable != "ConversionRate")) +
  geom_bar(aes(x = city_country, y = value, fill = variable), 
           stat = "identity",
           position = "fill") +
  geom_text(data = s1_ggdata %>%
              filter(variable == "ConversionRate"),
            aes(x = city_country, 
                y = 0.5, 
                group = variable, 
                label = as.character(paste(round(value,2), "%"))),
            position = "identity",
            colour = "white",
            fontface = "bold") +
  scale_fill_manual(values = c("#6438EA", "#28CF5D"),
                    labels = c("Visits", "Conversions")) +
  facet_wrap(~cr_category) +
  labs(x = "Location", 
       y = "Proportion",
       fill = "Metric") +
  theme(axis.text.x = element_text(angle = 45,
                                   hjust = 1)) +
  coord_flip()




