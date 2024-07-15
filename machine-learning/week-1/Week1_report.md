# Fraud Detection Report

## Approach

1. **Data Preparation:**
   - **Data Loading:** Downloaded and extracted the dataset using Kaggle API.
   - **Initial Exploration:** Inspected the dataset for unique values and checked for null values.
   - **Feature Engineering:**
     - Removed unnecessary ID columns.
     - Converted categorical columns to one-hot encoded features.
     - Added new features based on the relative values of transaction amount to account balances and their logarithms.

2. **Data Normalization:**
   - Normalized numerical columns by subtracting the mean and dividing by the standard deviation.

3. **Data Splitting:**
   - Split the dataset into training and testing sets using an 80-20 split.
   - Performed undersampling to balance the dataset due to the imbalance between fraud and non-fraud examples.

4. **Model Training and Evaluation:**
   - Trained multiple models: XGBoost, Random Forest, SVM, Neural Network, and Logistic Regression.
   - Evaluated models using accuracy, F1 score, and ROC AUC score.
   - Plotted confusion matrices for visual inspection of model performance.

## Challenges

- **Class Imbalance:** The dataset had a significant imbalance between fraud and non-fraud transactions, which required undersampling to ensure balanced training.
- **Feature Engineering:** Identifying and creating meaningful features to improve model performance.
- **Model Selection:** Evaluating different models to find the best performing one for the task.

## Results

- **XGBoost:** Achieved the highest performance with an accuracy of 99.96% and an F1 score of 0.87.
- **Random Forest:** Performed well with an accuracy of 99.92% and an F1 score of 0.78.
- **SVM:** Showed poor performance with an F1 score of 0.10, indicating it is not suitable for this task.
- **Neural Network:** Moderate performance with an F1 score of 0.25.
- **Logistic Regression:** Lowest performance with an F1 score of 0.06.

### Model Performance Summary

| Model                | Accuracy | F1 Score | ROC AUC Score |
|----------------------|----------|----------|---------------|
| XGBoost              | 99.96%   | 0.87     | 0.9998        |
| Random Forest        | 99.92%   | 0.78     | 0.9996        |
| SVM                  | 97.82%   | 0.10     | 0.9878        |
| Neural Network       | 99.25%   | 0.25     | 0.9953        |
| Logistic Regression  | 96.30%   | 0.06     | 0.9799        |

## Conclusion

The XGBoost model outperformed other models in detecting fraudulent transactions, making it the best choice for this task. Future work could involve exploring more advanced techniques for handling class imbalance and further tuning of model hyperparameters.

