# vanguard-ab-test

## Presentation:

- [Presentation](https://docs.google.com/presentation/d/17kFtHsBHe6cixQJJVP9lBWvgB--MVYXF6C_OogNpTfc/edit?usp=sharing)

## Tableau Public:

- [Tableau Public](https://public.tableau.com/views/vanguard_ab_test_17294341160880/Dashboard1?:language=de-DE&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

# Vanguard A/B Test Analysis

This repository contains code and resources for analyzing the results of an A/B test conducted for Vanguard. The analysis focuses on understanding user behavior, error rates, and overall performance between a control group and a test group.

## Overview

Vanguard, a leading investment management company, implemented a new and modern UI with the goal of creating a smoother online process for their clients. We examined data from an A/B test comparing Vanguard’s traditional online process to the new design to assess if the new UI leads to a better user experience and higher completion rates. Additionally, we analyzed the experiment itself to determine if it was well-structured and randomized to meet established statistical standards.

## Installation

To get started with this project, ensure you have the following libraries installed in your Python environment:

- `pandas` - For data manipulation and analysis
- `numpy` - For numerical operations
- `scipy` - For statistical tests
- `matplotlib` - For data visualization
- `seaborn` - For statistical data visualization

You can install these libraries using the following command:

pip install pandas numpy scipy matplotlib seaborn

## Objective

The objective of this project is to evaluate the performance of a new feature introduced in the test group compared to the control group. The key variables explored include:

- **Completion Rates**: The amount of users successfully navigating through the new vs the old design.
- **Error Rates**: The frequency of errors occurring during user interactions.
- **Time Spent**: The amount of time users spend on various steps in the process.

## Data Sources

The datasets used in this project include:

- **Client Demographics**: The file `df_final_demo.txt` contains client information and demographics, providing insights into the characteristics of the users.
  
- **Group Allocation**: The file `df_final_experiment_clients.txt` indicates the assignment of clients to either the test or control group, essential for understanding the experimental design.

- **User Interaction Data**: The files `df_final_web_data_pt_1.txt` and `df_final_web_data_pt_2.txt` include detailed logs of online behavior from clients, capturing their interactions during the A/B test.


## Data Overview and Handling
We were given four separate datasets:
- A dataset with general client information, including age, gender, account balance, and tenure.
- A dataset detailing which client IDs belonged to either the test or control group.
- A dataset containing all the logged online behavior of each client visit.

### Data Cleaning
We cleaned the dataset by:
- Removing null values and duplicates.
- Excluding client IDs that were not part of the experiment.
- Recasting some data types.
- Removing certain outliers for better visualization.

We merged the data on client IDs, created a control and test dataframe for analysis, and later developed a comprehensive dataframe containing everything for use in Tableau.

## Exploratory Data Analysis (EDA)
- **Age Distribution**: We have a bimodal distribution, with most clients being either between 30-35 or 50-55 years old. The mean and median age are both around 47 years, indicating that most clients tend to be above middle age.
- **Gender Distribution**: There is a relatively even gender distribution among male, female, and unknown, each comprising about a third of the clients.
- **Tenure**: Most users tend to have been clients for around 6 years, with a tenure mean of 12 and a median of 11 years, indicating that over 50% are longstanding users with more than 11 years of tenure.
- **Account Balance**: The account balance distribution is heavily positively skewed. After removing extreme outliers, the mean sits at 147,446 while the median is significantly lower at 63,334. Gender-wise, the distribution is relatively even, although extreme outliers belonged mostly to men. Individuals with unknown gender have a significantly lower mean and median.
- **Longevity**: Men and women appear to be similarly longstanding customers, while those with unknown gender tend to be relatively new customers, likely because longstanding customers have more interactions with staff where their gender might be recorded.

## KPI and Performance Metrics
To evaluate the new design’s performance, we looked at three main KPIs:
1. **Completion Rate**: Percentage of clients reaching “confirm” per visit.
2. **Error Rate**: Each time a client took a step backward compared to the total number of actions.
3. **Time Spent per Step**: The average time a client spent on each step.

We also calculated the error ratio for each step to identify optimization opportunities.

### Overall Performance
- The new design performed better, especially in the key KPI of completion rate, with some caveats:
  - The error rate in the new UI was overall slightly higher than in the old design.
  - Step one of the new online process seems to have been a downgrade, with clients taking longer and making more errors compared to the classic interface.
  
When these flaws are addressed, the new UI could be a definitive improvement.

## Hypothesis Testing
- **Null Hypothesis (H0)**: The updated design did not improve the completion rate.
- **Alternative Hypothesis (H1)**: The updated design led to a higher completion rate.
- **Significance Level (α)**: 0.05

Using a proportions z-test, we could reject the null hypothesis. The increase in completion rate exceeded the 5% threshold set by Vanguard, justifying the new design from a cost perspective.

## Experiment Evaluation
We evaluated the experiment for adequate size, structure, and randomization to identify any relevant biases:
- Is the average age of clients engaging with the new process the same as those engaging with the old process?
- Is the average client tenure (time with Vanguard) the same for clients engaging with the new process compared to the old process?
- Are there gender differences affecting client engagement with the new or old process?

Both samples were sufficiently large and similar (test group: 176,699 rows / control group: 140,536 rows), leading us to conclude that the timeframe for data gathering was adequate. 

While the differences were statistically significant according to their p-values, the Cohen's values were small enough to suggest the differences are minimal in terms of effect size. In conclusion, the raw data between the control and test groups is overall randomly distributed with minimal bias.

## Conclusion
The new design is an overall success, particularly among older clients. Improvements should be made specifically to step 1. The experiment was well-structured and exhibited little bias, making the implementation cost-effective. 

We recommend that Vanguard address minor issues before proceeding with the full implementation of the new UI.


