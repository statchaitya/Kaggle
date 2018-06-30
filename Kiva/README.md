## Kaggle - Data Science for Good
## Data Visualization and analysis competition
## About Kiva

Kiva.org is an online crowdfunding platform to extend financial services to poor and financially excluded people around the world. Kiva lenders have provided over $1 billion dollars in loans to over 2 million people. In order to set investment priorities, help inform lenders, and understand their target communities, knowing the level of poverty of each borrower is critical. However, this requires inference based on a limited set of information for each borrower.

## Problem Statement

For the locations in which Kiva has active loans, your objective is to pair Kiva's data with additional data sources to estimate the welfare level of borrowers in specific regions, based on shared economic and demographic characteristics.

A good solution would connect the features of each loan or product to one of several poverty mapping datasets, which indicate the average level of welfare in a region on as granular a level as possible. Many datasets indicate the poverty rate in a given area, with varying levels of granularity. Kiva would like to be able to disaggregate these regional averages by gender, sector, or borrowing behavior in order to estimate a Kiva borrower’s level of welfare using all of the relevant information about them. Strong submissions will attempt to map vaguely described locations to more accurate geocodes.

Kernels submitted will be evaluated based on the following criteria:

1. Localization - How well does a submission account for highly localized borrower situations? Leveraging a variety of external datasets and successfully building them into a single submission will be crucial.

2. Execution - Submissions should be efficiently built and clearly explained so that Kiva’s team can readily employ them in their impact calculations.

3. Ingenuity - While there are many best practices to learn from in the field, there is no one way of using data to assess welfare levels. It’s a challenging, nuanced field and participants should experiment with new methods and diverse datasets.

## My solution description

Philippines is the country with the most number of loans in the data. I decided to focus on identifying those areas in philippines which were more needy in terms of loan (economically backward) so that perhaps more loans could be diverted to these regions in the future than regions where the richer category of people live. I searched for an online economic indicators data about the regions in Philippines, cleaned it to bring in appropriate form and joined it with the Kaggle data to perform analysis.

Data files for this data can be found at the following links. To reproduce the analysis, run the .R files after downloading the data files from here

https://www.kaggle.com/kiva/data-science-for-good-kiva-crowdfunding

https://www.kaggle.com/statchaitya/a-few-poverty-indicators-for-philippines-by-region

https://www.kaggle.com/statchaitya/philippines-regions-and-provinces
