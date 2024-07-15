# Customer Segregation Report

## Introduction

This report summarizes the approach, challenges, and results of the customer segregation task performed using a marketing campaign dataset. The objective was to cluster customers based on their demographic and purchasing behavior to facilitate targeted marketing strategies.

## Approach

1. **Data Loading and Preprocessing**:
    - **Dataset**: The dataset was loaded, and initial exploration was performed to understand its structure and contents.
    - **Handling Missing Values**: Rows with missing values were dropped to ensure data quality.
    - **Data Cleaning**: 
        - Outliers in the `Income` column were filtered out.
        - The `Year_Birth` column was corrected for any erroneous values and converted into an `Age` column.
        - The `Education` column was simplified and one-hot encoded for better processing.

2. **Exploratory Data Analysis (EDA)**:
    - The dataset was explored to identify unique values and distributions in various columns.
    - Key transformations included simplifying categorical columns and encoding them appropriately.

3. **Feature Engineering**:
    - Standardization of numerical features to bring them to a similar scale.
    - Principal Component Analysis (PCA) was performed to reduce dimensionality while retaining most of the variance.

4. **Clustering**:
    - Various clustering algorithms, including K-Means, DBSCAN, and Agglomerative Clustering, were applied.
    - The optimal number of clusters was determined using techniques such as the Elbow Method.

5. **Visualization**:
    - Clusters were visualized using PCA to project high-dimensional data into two dimensions.
    - Different clustering results were compared and analyzed.

## Results

- PCA helped in reducing dimensionality, making it easier to visualize and interpret the clusters.
- K-Means clustering with an optimal number of clusters (determined through the Elbow Method) provided meaningful customer segments.
- Visualization of the clusters revealed distinct groups of customers, aiding in targeted marketing strategies.
