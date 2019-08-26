########################## Exploring google merchandise data ###################################

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


glimpse(dtrain)


dtrain %>% count(channelGrouping)
###########
# What is the conversion rate in channelGrouping?

dtrain %>% group_by(channelGrouping) %>%
  summarise(totalConversions = sum(transactionRevenueNew > 0),
            totalSessions = n()) %>%
  mutate(ConversionRate = (totalConversions/totalSessions)*100) %>%
  arrange(ConversionRate)

# Referral has the highest CR 5.07% followed by display and paid search at 2.27% and 1.85% respectively.

##########

# What is the prominent location in referrals?

dtrain %>% filter(channelGrouping == "Referral") %>%
  group_by(city, country) %>%
  summarise(totalConversions = sum(transactionRevenueNew > 0),
            totalSessions = n(),
            totalRevenue = sum(transactionRevenueNew)) %>%
  mutate(ConversionRate = (totalConversions/totalSessions)*100) %>%
  filter(totalSessions > 1000) %>%
  arrange(desc(totalRevenue))

# Within referrals, ann arbor, chicago and New york had the highest conversion rate of 14.5%, 13% and 10.6%
# .. respectively with New york having a highest total revenue among these 3, which is 132990.

# Among cities having > 1000 referral visits, Unknwon city in Japan, London, UK, Palo Alto US had the least
# .. conversion rates.

# Reccomendation: Curtail referral campaigns to above 3 locations. Increase campaign and referral traffic from
# .. locations mentioned in comment 1.

#################################################
# General Details on referral marketing and referral traffic
# Referral marketing campaigns are campaigns that incentivize your customers to refer your products to their 
# ..family, friends, or colleagues. Referral marketing campaigns are in essence a way to turn your customers 
# ..and fans into brand advocates.
# 
# Referral traffic in Google Analytics is a recommendation from one site to another. 

#################################################
dtrain %>% filter(channelGrouping == "Referral") %>%
  group_by(deviceCategory) %>%
  summarise(totalConversions = sum(transactionRevenueNew > 0),
            totalSessions = n(),
            totalRevenue = sum(transactionRevenueNew)) %>%
  mutate(ConversionRate = (totalConversions/totalSessions)*100) %>%
  arrange(desc(totalRevenue))


# conversion rate for referrals in mobile is 0.2% where as that in desktop is 5.34%.

##########
# PAID SEARCH CAMPAIGN

dtrain %>% filter(channelGrouping == "Referral") %>% count(campaign)


dtrain %>% group_by(campaign, channelGrouping) %>%
  summarise(totalConversions = sum(transactionRevenueNew > 0),
            totalSessions = n()) %>%
  mutate(ConversionRate = (totalConversions/totalSessions)*100) %>%
  arrange(desc(ConversionRate)) %>%
  filter(campaign != "(not set)", totalSessions > 300)

# Referral has no campaign associated with it (campaign = (not set)).
# Campaigning through Affiliates is not working. It has a conversion rate of .5%
# Among paid search, "AW-Dynamic search ads whole site" campaign has hi'est conversion rate of 2.27%

########################################################################################
# Q. Which is the most successful and unsuccessful paid search campaign

dtrain %>% 
  filter(channelGrouping == "Paid Search") %>%
  group_by(campaign, channelGrouping) %>%
  summarise(totalConversions = sum(transactionRevenueNew > 0),
            totalSessions = n(),
            totalRevenue = sum(transactionRevenue)) %>%
  filter(totalSessions > 300) %>%
  mutate(ConversionRate = (totalConversions/totalSessions)*100) %>%
  arrange(desc(ConversionRate))

# Considering only the campaigns with visits > 300, "AW - Dynamic Search ads whole site" had highest CR. AW - Accessories was close
# .. 2nd with 1.84 CR

# What are characteristics of sessions coming in from DSAds vs. normal Ad words ads
dynamic_vs_normal_adwords_comparison <- 
  dtrain %>% 
    filter(channelGrouping == "Paid Search") %>% 
    mutate(AdType = if_else(grepl("Dynamic Search", campaign), "Paid Search - Dynamic", "Paid Search - Adwords")) %>%
    group_by(AdType) %>%
    summarise(totalConversions = sum(transactionRevenueNew > 0),
              totalSessions = n(),
              totalRevenue = sum(transactionRevenue),
              uniqueDays = n_distinct(date),
              uniqueVisitors = n_distinct(fullVisitorId),
              mobileVisits = sum(deviceCategory == "mobile"),
              desktopVisits = sum(deviceCategory == "desktop"),
              tabletVisits = sum(deviceCategory == "tablet"),
              usaVisits = sum(country == "United States"),
              indiaVisits = sum(country == "India"),
              ukVisits = sum(country == "United Kingdom"),
              canadaVisits = sum(country == "Canada"),
              totalPageViews = sum(pageviews),
              totalBounces = sum(bounces),
              totalNewVisits = sum(newVisits))

dynamic_vs_normal_adwords_comparison_melted <- melt(dynamic_vs_normal_adwords_comparison)

dynamic_vs_normal_adwords_comparison_plot <-  ggplot(data = dynamic_vs_normal_adwords_comparison_melted %>%
                                                       filter(variable != "totalRevenue")) +
    geom_bar(aes(x = variable, y = value, fill = AdType),
             position = "stack",
             stat = "identity") +
    labs(x = "Metric",
         y = "Proportion") +
    scale_fill_manual(values = c("#38CFEA", "#6438EA")) +
    theme(axis.text.x = element_text(angle = 45,
                                     hjust = 1,
                                     vjust = 1))
ggplotly(
  dynamic_vs_normal_adwords_comparison_plot)


# IDeas for future. 
# 1. Calculate pageviews/session and compare paid searches
# 2. Calculate bounce rate
# 3. New Visit Rate
# 4. Inter device CR per adtype?
# 5. Research more metrics

ggplot(dynamic_vs_normal_adwords_comparison_melted %>%
         filter(variable == "totalSessions") %>%
         arrange(desc(AdType)) %>%
         mutate(lab.ypos = cumsum(value) - 0.5*value), 
       aes(x="", y=value, fill=AdType)) +
  geom_bar(width = 1, stat = "identity", color="white") +
  coord_polar("y", start = 0) +
  geom_text(aes(y = lab.ypos, label = value), color = "white")+
  scale_fill_manual(values = c("#0073C2FF", "#EFC000FF")) +
  theme_void()

dtrain %>% 
  filter(channelGrouping == "Paid Search", campaign == "AW - Dynamic Search Ads Whole Site") %>%
  group_by(city, country) %>% 
  summarise(totalConversions = sum(transactionRevenueNew > 0),
            totalSessions = n(),
            totalRevenue = sum(transactionRevenue)) %>%
  filter(totalSessions > 100) %>%
  mutate(ConversionRate = (totalConversions/totalSessions)*100) %>%
  arrange(ConversionRate)


##########

channelAndCampaignDF <- dtrain %>% mutate(channelAndCampaign = paste(channelGrouping, campaign)) %>%
        group_by(channelAndCampaign) %>%
        summarise(totalConversions = sum(transactionRevenueNew > 0),
                  totalSessions = n(),
                  uniqueDays = n_distinct(date),
                  uniqueVisitors = n_distinct(fullVisitorId),
                  mobileVisits = sum(deviceCategory == "mobile"),
                  desktopVisits = sum(deviceCategory == "desktop"),
                  tabletVisits = sum(deviceCategory == "tablet"),
                  usaVisits = sum(country == "United States"),
                  indiaVisits = sum(country == "India"),
                  ukVisits = sum(country == "United Kingdom"),
                  canadaVisits = sum(country == "Canada"),
                  totalPageViews = sum(pageviews),
                  totalBounces = sum(bounces),
                  totalNewVisits = sum(newVisits)) %>%
        mutate(ConversionRate = (totalConversions/totalSessions)*100) %>%
        select(channelAndCampaign, ConversionRate, everything()) %>%
        arrange(desc(ConversionRate))
  

library(formattable)

formatters <- list(ConversionRate = color_tile("#DeF7E9", "#71CA97"),
                   totalConversions = color_tile("#DeF7E9", "#71CA97"),
                   totalSessions = color_tile("#DeF7E9", "#71CA97"),
                   uniqueDays = color_tile("#DeF7E9", "#71CA97"),
                   uniqueVisitors = color_tile("#DeF7E9", "#71CA97"),
                   mobileVisits = color_tile("#DeF7E9", "#71CA97"),
                   desktopVisits = color_tile("#DeF7E9", "#71CA97"),
                   tabletVisits = color_tile("#DeF7E9", "#71CA97"),
                   usaVisits = color_tile("#DeF7E9", "#71CA97"),
                   indiaVisits = color_tile("#DeF7E9", "#71CA97"),
                   ukVisits = color_tile("#DeF7E9", "#71CA97"),
                   canadaVisits = color_tile("#DeF7E9", "#71CA97"),
                   totalPageViews = color_tile("#DeF7E9", "#71CA97"),
                   totalBounces = color_tile("#DeF7E9", "#71CA97"),
                   totalNewVisits = color_tile("#DeF7E9", "#71CA97"))

formattable(channelAndCampaignDF,
            align = rep("c", 16),
            formatters)
            
# Next steps

# Gather insights and create hypothesis from formattable data

################

# Exclusively when analyzing channelAndCampaign | level - channelAndCampaign, fullVisitorId
repeatVisitorDF <- dtrain %>% mutate(channelAndCampaign = paste(channelGrouping, campaign)) %>%
      group_by(channelAndCampaign, fullVisitorId) %>% # PSC1 - visitor 1 - 10 sessions
      summarise(repeatVisitor = if_else(min(visitNumber) > 1, "Repeat Visitor", "New Visitor"))
