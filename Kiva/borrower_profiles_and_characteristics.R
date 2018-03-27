
setwd("C:/Kaggle/kiva/")

# read in the data
kiva_loans <- read.csv("kiva_loans.csv", header=T)
kiva_regions <- read.csv("kiva_mpi_region_locations.csv", header=T)
loan_theme_ids <- read.csv("loan_theme_ids.csv", header=T)
loan_theme_regions <- read.csv("loan_themes_by_region.csv", header=T)

library(dplyr)
library(ggplot2)

# For the locations in which KIVA has active loans
# --> Where are the maximum no. of loans getting disbursed?
#     Suppose pakistan is one of the countries where the loans are getting disbursed,
# --> What borrower profiles (a particular activity/sector/gender/payment_per_month bracket)
#     exist? What are their characteristics w.r.t three metrics.
# First let us locate particular segments and then lets check their

# Top 10 locations (countries) where the loans are getting disbursed
# Location variables? --> country, region,

# Top 10 countries

              
        
ggplot(data = kiva_loans %>% group_by(country) %>% 
                 summarise(row_count = n_distinct(id)) %>%
                 top_n(20, row_count),
               aes(x = reorder(country, row_count), y = row_count)) +
          geom_bar(stat = "identity", width = 0.5, fill = "red", colour = "black") +
    scale_x_discrete("Country") + scale_y_continuous("Number of Loans Disbursed") +
          theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5),
    axis.title.y = element_text(face = "bold"), 
    axis.title.x = element_text(face = "bold")) +
    coord_flip()

# Total % of loans disbursed in top5 countries relative to total loans?

top_5_country_loan_count <- as.numeric(kiva_loans %>% filter(country %in% c("Philippines", 
                                     "Kenya",
                                    "El Salvador",
                                    "Cambodia",
                                    "Pakistan")) %>%
                summarise(n_distinct(id))
           )
total_loan_count <- length(unique(kiva_loans$id))

cat(paste("The top 5 countries cover", 
      paste(round((top_5_country_loan_count/total_loan_count),2)*100,"%",sep="") ,
      "of the total loans disbursed by KIVA so we will focus on these countries for now", sep =" "))

# Let us consider only the top 5 countries for now.
# Create a separate data frame for these top 5 countries

kiva_loans_top5 <- data.frame(kiva_loans %>% filter(country %in% c("Philippines", 
                                                        "Kenya",
                                                        "El Salvador",
                                                        "Cambodia",
                                                        "Pakistan")))

kiva_loans_top5$gender <- if_else((kiva_loans_top5$borrower_genders == "male"), "male","female")
kiva_loans$gender <- if_else((kiva_loans$borrower_genders == "male"), "male","female")
# EDA of top 5 countries
names(kiva_loans_top5)
# what are the top sectors in which the loans are getting allotted?

ggplot(data = kiva_loans_top5 %>% group_by(sector) %>% 
         summarise(row_count = n_distinct(id)) %>%
         top_n(20, row_count),
       aes(x = reorder(sector, row_count), y = row_count)) +
  geom_bar(stat = "identity", width = 0.5, fill = "blue", colour = "black") +
  scale_x_discrete("Sector") + scale_y_continuous("Number of Loans Disbursed") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5),
        axis.title.y = element_text(face = "bold"), 
        axis.title.x = element_text(face = "bold")) +
  coord_flip()

# What % do the top 8 sectors cover?
top_8_sector_perc <- (as.numeric(kiva_loans_top5 %>% filter(sector %in% c("Agriculture", 
                                                                     "Retial",
                                                                     "Food",
                                                                     "Personal Use",
                                                                     "Services",
                                                                     "Housing",
                                                                     "Clothing",
                                                                     "Transportation")
                                                                  ) %>%
                                  summarise(n_distinct(id))
        )/ length(unique(kiva_loans_top5$id)))*100

cat(paste(paste("The top 8 sectors cover", paste(round(top_8_sector_perc,2),"%", sep =""), "of the data", sep = " "), "so we will focus on these sectors first", sep = " "))

# How do the loan amt, term do w.r.t some top sectors in each country?
# w.r.t noz


# Median loan amount in cambodia is high for transportation & Clothing and lowest
# for personal use
ggplot(kiva_loans_top5 %>%
         filter(sector %in% c("Agriculture", 
                              "Retail",
                              "Food",
                              "Personal Use",
                              "Services",
                              "Housing",
                              "Clothing",
                              "Transportation")) %>% 
         group_by(country, sector) %>%
         summarise(loanAmt_median = median(loan_amount)), aes(x = country, loanAmt_median)) +   
  geom_bar(aes(fill = sector), colour = "black", 
            width = 0.8, position = "dodge", stat="identity")


# Observations:
# We can see that MEDIAN(LOAN AMOUNTS) are low for PERSONAL USE sector in CAMBODIA, KENYA, PHILIPPINEs
# Lets see what are the top ACTIVITIES in sector PERSONAL USE



ggplot(data = kiva_loans_top5 %>% filter(sector == "Personal Use") %>%
         group_by(activity) %>% summarise(row_count = n_distinct(id)) %>% 
         top_n(20, row_count),
       aes(x = reorder(activity, row_count), y = row_count)) +
  geom_bar(stat = "identity", width = 0.5, fill = "green", colour = "black") +
  scale_x_discrete("Activities under Sector: Personal Use") + 
  scale_y_continuous("Number of Loans Disbursed") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5),
        axis.title.y = element_text(face = "bold"), 
        axis.title.x = element_text(face = "bold")) +
  coord_flip()

# How are the same country/sector groups doing w.r.t term?
ggplot(kiva_loans_top5 %>%
         filter(sector %in% c("Agriculture", 
                              "Retail",
                              "Food",
                              "Personal Use",
                              "Services",
                              "Housing",
                              "Clothing",
                              "Transportation")) %>% 
         group_by(country, sector) %>%
         summarise(loanTerm_median = median(term_in_months)), aes(x = country, loanTerm_median)) +   
  geom_area(aes(fill = sector), colour = "black", 
           width = 0.8, position = "dodge", stat="identity")

# Loan Amounts by gender
ggplot(kiva_loans_top5 %>%
         filter(sector %in% c("Agriculture", 
                              "Retail",
                              "Food",
                              "Personal Use",
                              "Services",
                              "Housing",
                              "Clothing",
                              "Transportation")) %>% 
         group_by(country, sector, gender) %>%
         summarise(loanAmt_median = median(loan_amount)), aes(x = country, loanAmt_median)) +   
  geom_bar(aes(fill = sector), colour = "black", 
           width = 0.8, position = "dodge", stat="identity") +
  facet_grid(gender ~.)

# Loan terms by gender
ggplot(kiva_loans_top5 %>%
         filter(sector %in% c("Agriculture", 
                              "Retail",
                              "Food",
                              "Personal Use",
                              "Services",
                              "Housing",
                              "Clothing",
                              "Transportation")) %>% 
         group_by(country, sector, gender) %>%
         summarise(loanTerm_median = median(term_in_months)), aes(x = country, loanTerm_median)) +   
  geom_bar(aes(fill = sector), colour = "black", 
           width = 0.8, position = "dodge", stat="identity") +
  facet_grid(gender ~.)



