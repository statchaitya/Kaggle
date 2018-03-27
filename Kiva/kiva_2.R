# Kiva exploration part 2

setwd("C:/Kaggle/kiva/")

# read in the data
kiva_loans <- read.csv("kiva_loans.csv", header=T)
kiva_regions <- read.csv("kiva_mpi_region_locations.csv", header=T)
loan_theme_ids <- read.csv("loan_theme_ids.csv", header=T)
loan_theme_regions <- read.csv("loan_themes_by_region.csv", header=T)


library(dplyr)
library(ggmap)
library(mapdata)
library(maps)
library(ggplot2)



# creating new variable
kiva_loans$payment_per_month <- kiva_loans$loan_amount/kiva_loans$term_in_months

summary(kiva_loans$payment_per_month)

# 0-5% ppm (0-4$/0-250 Rs. ppm) -> strugglers
# 5-25% ppm (4-25$/ 250-1600 Rs. ppm)-> fighters
# 25-60% ppm (26-47$ / 1600-3000 Rs. ppm) -> good
# 60-85% PPM (48-100$ / 3000-6500 Rs. ppm) -> better
# 85-100% ppm (100$ + ) -> best

# creating new factor welfare_status
kiva_loans$welfare_status <- case_when(
  kiva_loans$payment_per_month <= 4 ~ "very low ppm",
  kiva_loans$payment_per_month > 4 & kiva_loans$payment_per_month <= 25 ~ "low ppm",
  kiva_loans$payment_per_month > 25 & kiva_loans$payment_per_month <= 47 ~ "average ppm",
  kiva_loans$payment_per_month > 47 & kiva_loans$payment_per_month <= 100 ~ "good ppm",
  kiva_loans$payment_per_month > 100 ~ "very good ppm",
  TRUE ~ "Other")

# Checking if everything is fine
# % in each class
round(prop.table(table(kiva_loans$welfare_status))*100,2)

# Top 20 lowest countries with median payment per month
bottom_20_ppm_country_df <- data.frame((kiva_loans %>% 
                                              group_by(country) %>% 
                                          summarise(ppm_median = median(payment_per_month)) %>% 
                                            arrange(ppm_median))[1:20,])
# Sorting the df so that the barplot is ordered
bottom_20_ppm_country_df$country <- factor(
        bottom_20_ppm_country_df$country, 
            levels = bottom_20_ppm_country_df$country[order(
                bottom_20_ppm_country_df$ppm_median)])


bottom_20_ppm_country_barplot <- ggplot(
            data = bottom_20_ppm_country_df, aes(x = country, y = ppm_median)) +
                  geom_bar(stat = "identity", width = 0.35, fill = "red", colour = "black") +
            scale_x_discrete("Country") +
          scale_y_continuous("Median $ Payment Per Month") +
        theme(axis.title.x = element_text(face = "bold", hjust = 0.5, vjust = 0), 
            axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.2),
            axis.title.y = element_text(face = "bold", vjust = 0.3),
            legend.key.size = unit(0.25, units = "cm"))

# REDUCE THE COUNTRY NAME AND COLORS SIZE LATER

plot(bottom_20_ppm_country_barplot)

## top 20 lowest median loan taking countries
bottom_20_loanamt_country_df <- data.frame((kiva_loans %>% 
                                              group_by(country) %>% 
                                              summarise(loanamt_median = median(loan_amount)) %>% 
                                              arrange(loanamt_median))[1:20,])
# Sorting the df so that the barplot is ordered
bottom_20_loanamt_country_df$country <- factor(
  bottom_20_loanamt_country_df$country, 
  levels = bottom_20_loanamt_country_df$country[order(
    bottom_20_loanamt_country_df$loanamt_median)])


bottom_20_loanamt_country_barplot <- ggplot(
  data = bottom_20_loanamt_country_df, aes(x = country, y = loanamt_median, fill = country)) +
  geom_bar(stat = "identity", width = 0.35, fill = "green", colour = "black") +
  scale_x_discrete("Bottom 20 Countries") +
  scale_y_continuous("Median $  Loan  Amount") +
  theme(axis.title.x = element_text(face = "bold", hjust = 0.5, vjust = 0), 
        axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.2),
        axis.title.y = element_text(face = "bold", vjust = 0.3),
        legend.key.size = unit(0.25, units = "cm"))

plot(bottom_20_loanamt_country_barplot)

## bottom_20_countries_w.r.t_loan_term

bottom_20_loanterm_country_df <- data.frame((kiva_loans %>% 
                                                  group_by(country) %>% 
                                                  summarise(loanterm_median = median(term_in_months)) %>% 
                                                  arrange(loanterm_median))[1:20,])
# Sorting the df so that the barplot is ordered
bottom_20_loanterm_country_df$country <- factor(
  bottom_20_loanterm_country_df$country, 
  levels = bottom_20_loanterm_country_df$country[order(
    bottom_20_loanterm_country_df$loanterm_median)])


bottom_20_loanterm_country_barplot <- ggplot(
  data = bottom_20_loanterm_country_df, aes(x = country, y = loanterm_median, fill = country)) +
  geom_bar(stat = "identity", width = 0.35, fill = "blue", colour = "black") +
  scale_x_discrete("Bottom 20 Countries") +
  scale_y_continuous("Median term in months") +
  theme(axis.title.x = element_text(face = "bold", hjust = 0.5, vjust = 0), 
        axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.2),
        axis.title.y = element_text(face = "bold", vjust = 0.3),
        legend.key.size = unit(0.25, units = "cm"))

plot(bottom_20_loanterm_country_barplot)







# Importing WID data shared by the user PETER.
countries <- read.csv("C:/Kaggle/kiva/External_Data/data_2_wid/countries.csv"
                      , header=T)
wid <- read.csv("C:/Kaggle/kiva/External_Data/data_2_wid/wid.csv"
                , header=T)
wid_vars <- read.csv("C:/Kaggle/kiva/External_Data/data_2_wid/wid_variables.csv",
                     header=T)


