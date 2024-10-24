# Medication Combination Effectiveness Study for Diabetes Patients

## Overview
This project explores the effectiveness of various combinations of diabetes medications on patient outcomes, particularly focusing on hospital readmission rates. Using **Support Vector Machine (SVM)** and other statistical models, the study analyzes patterns in medication usage and their impact on patients. The medications analyzed include metformin, glipizide, glyburide, insulin, and more, with a special emphasis on combinations that can reduce hospital readmission.

## Key Objectives
- **Analyze Medication Effectiveness**: Investigate the impact of different diabetic medication combinations on patient outcomes.
- **Readmission Prediction**: Use predictive modeling to understand how medication affects hospital readmission rates, identifying key patterns and relationships between drugs.

## Data Insights
The dataset reveals that:
- **Metformin** and other medications like **Glipizide** and **Glyburide** exhibit heavily skewed usage, with the majority of patients not prescribed these drugs.
- **Insulin** usage shows a more balanced distribution, indicating frequent use and adjustments, providing better insights into its impact on outcomes.
- Medications such as **Repaglinide**, **Nateglinide**, and **Acetohexamide** are rarely prescribed, contributing little to predictive models due to the lack of data variability.

## Key Findings
- **Insulin** plays a critical role in managing diabetes, with its usage linked to more stable patient outcomes.
- **Metformin & Nateglinide** and **Insulin & Acetohexamide** combinations are shown to significantly reduce readmission rates.
- In contrast, medications like **Tolbutamide** and **Chlorpropamide** are rarely used and have little impact on patient outcomes.

## Analytical Approach
- **Violin and Box Plots**: Used to display the distribution of medication dosages and detect outliers in drug usage.
- **Correlation Matrix**: Provides insights into the relationships between different medications and their collective impact on patient readmission.
- **Bivariate & Multivariate Regression**: Used to evaluate the strength of the relationship between specific medications and readmission rates. Despite statistical significance, the low R-squared values suggest other factors beyond medication influence readmission.

## Conclusion
The study highlights the importance of maintaining consistent medication dosages to improve patient outcomes. While certain medications like **Insulin** and **Metformin** are critical in reducing readmission rates, the overall predictive power of the models is low, suggesting the need for further research into other factors affecting patient outcomes.

## How to Run
1. Clone the repository.
2. Prepare the dataset as described in the documentation.
3. Run the SVM and regression models using Python or other statistical tools.
4. Analyze the outputs to explore the relationships between medication usage and patient readmission rates.

## Technologies Used
- **Python**: For data analysis and predictive modeling.
- **SVM (Support Vector Machine)**: To detect patterns in medication usage.
- **Pandas** and **Matplotlib**: For data manipulation and visualization.
- **Violin Plots, Box Plots**: For visualizing data distributions and outliers.
