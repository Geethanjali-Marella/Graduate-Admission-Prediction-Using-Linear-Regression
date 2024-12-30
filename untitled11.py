# -*- coding: utf-8 -*-
"""Untitled11.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YPX_ig2HoNxBzPT3kLf8MHYhLayUjiX1
"""

import pandas as pd
import numpy as np

df = pd.read_csv("Jamboree_Admission.csv")
df.head()

df.info()

"""**Seems No null values occurs in our data **"""

df.duplicated().sum()

"""No duplicates exist in our data set"""

df.describe()

df.shape

#Checking Outliers


q1 = df.quantile(0.25)
q2 = df.quantile(0.5)
q3 = df.quantile(0.75)

IQR = q3-q2

# Using IQR to filter out outliers
df_filtered = df[~((df < q1-IQR*1.5)  | (df> q3+ 1.5*IQR)).any(axis = 1)]
df_filtered.shape

"""**After handling with ouliers, we reduced the rows in dataset from 500 to 325**

**Dropping Serial No. column , to avoid our model may learn with according to row numbers**
"""

df_filtered.drop(columns = ['Serial No.'], inplace = True)
df_filtered

"""**Non Graphical Analysis**"""

df_filtered.describe()

"""variance says that, GRE and TOEFL scores are slightly distributed, compared to others.

mean and 50% almost same, says every column data distribution is skewed.

While comparing (25% and min)  and (75% and max) almost equal, says no outliers, as we already handled them

From count, we can say, that there are no null values.

**Graphical Analysis**
"""

# Plotting histograms for GRE and TOEFL Scores
import matplotlib.pyplot as plt
import seaborn as sns


plt.figure(figsize=(14, 5))
plt.subplot(1, 2,1)
sns.histplot(df_filtered['GRE Score'], bins=20, kde=True)
plt.title('Distribution of GRE Scores')

plt.subplot(1, 2, 2)
sns.histplot(df_filtered['TOEFL Score'], bins=20, kde=True)
plt.title('Distribution of TOEFL Scores')


plt.figure(figsize=(14, 5))
plt.subplot(2, 2,1)
sns.histplot(df_filtered['University Rating'], bins=20, kde=True)
plt.title('Distribution of University Rating')

plt.subplot(2, 2, 2)
sns.histplot(df_filtered['CGPA'], bins=20, kde=True)
plt.title('Distribution of CGPA')

plt.tight_layout()
plt.show()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Assuming df is your DataFrame
correlation_matrix = df_filtered.corr()

# Display the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation Matrix for Graduate Admissions Data')
plt.show()

"""**Seems, chance of admit is hihgly dependent on CGPA of college and GRE score, and leastly on LOR.**

**Linear Regression Model building**

1.Standarisation of data set, for effective results
"""

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df = pd.DataFrame(scaler.fit_transform(df_filtered), columns = df_filtered.columns)
df

"""2.splitting traiining data and test data"""

from sklearn.model_selection import train_test_split
y = df["Chance of Admit "]
x = df.drop(columns = ["Chance of Admit "])


X_train, X_test, Y_train, Y_test = train_test_split(x,y,test_size = 0.2, random_state=2)
X_train

import statsmodels.api as sm


y_train = np.array(Y_train)


# Add a constant to X_train for the intercept
X_sm = sm.add_constant(X_train)
print(X_sm.shape)

# Fit the model
model = sm.OLS(y_train, X_sm)
results = model.fit()
results.summary()

print(X_sm.shape)
results.params

"""**Based, on weights, we can say that, chance of admit purely impacts by TOEFL \, GRE scores and mostly on CGPA, very low impact by LOR and its inversly proporsional as well**"""

X_test_sm = sm.add_constant(X_test)

# Make predictions using the fitted model
y_hap = results.predict(X_test_sm)

# Display predictions
print(f"Predictions (y_hap): {y_hap}")

import matplotlib.pyplot as plt

# Plot actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(Y_test, y_hap, color='blue', alpha=0.6)
plt.plot([min(Y_test), max(Y_test)], [min(Y_test), max(Y_test)], color='red', linestyle='--')
plt.title("Actual vs Predicted Values")
plt.xlabel("Actual Values (Chance of Admit)")
plt.ylabel("Predicted Values (Chance of Admit)")
plt.show()

"""**Trying different regressions**"""

from sklearn.linear_model import Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score

# Prepare data (Ensure this is already done from your earlier code)
y = df["Chance of Admit "]
X = df.drop(columns=["Chance of Admit "])

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
# Initialize Ridge Regression model
ridge_model = Ridge(alpha=1.0)  # alpha is the regularization strength

# Fit the model
ridge_model.fit(X_train, y_train)

# Predict using the trained model
ridge_pred = ridge_model.predict(X_test)

# Evaluate the model
ridge_mse = mean_squared_error(y_test, ridge_pred)
ridge_r2 = r2_score(y_test, ridge_pred)

print(f"Ridge Regression - Mean Squared Error: {ridge_mse}")
print(f"Ridge Regression - R-squared: {ridge_r2}")

# Coefficients
print(f"Ridge Coefficients: {ridge_model.coef_}")

# Initialize Lasso Regression model
lasso_model = Lasso(alpha=0.1)  # alpha is the regularization strength

# Fit the model
lasso_model.fit(X_train, y_train)

# Predict using the trained model
lasso_pred = lasso_model.predict(X_test)

# Evaluate the model
lasso_mse = mean_squared_error(y_test, lasso_pred)
lasso_r2 = r2_score(y_test, lasso_pred)

print(f"Lasso Regression - Mean Squared Error: {lasso_mse}")
print(f"Lasso Regression - R-squared: {lasso_r2}")

# Coefficients
print(f"Lasso Coefficients: {lasso_model.coef_}")

"""**Assumptions**

1.Multicollinearity check by VIF score
"""

from statsmodels.stats.outliers_influence import variance_inflation_factor
vif = pd.DataFrame()
X_t = pd.DataFrame(X_train, columns=X_train.columns)
vif['Features'] = X_t.columns
vif['VIF'] = [variance_inflation_factor(X_t.values, i) for i in range(X_t.shape[1])]
vif['VIF'] = round(vif['VIF'], 2)
vif = vif.sort_values(by = "VIF", ascending = False)
vif

"""**High Multicollinearity:**

Features such as CGPA (20.93), GRE Score (18.91), TOEFL Score (16.53), University Rating (10.30), SOP (9.05), and LOR (5.06) all have high VIF values greater than 5, indicating multicollinearity. This suggests that these features are highly correlated with each other, which may cause issues in regression models

2.The mean of residuals is nearly zero
"""

# Assuming you have the model 'results' from statsmodels and 'X_sm' (with a constant term) and 'y_train'
residuals = y_train - results.predict(X_sm)

# Calculate mean of residuals
mean_residuals = np.mean(residuals)
print(f"Mean of Residuals: {mean_residuals}")

"""Since the mean of residuals is effectively zero, there is no indication of any issue in terms of model bias.

3.Linearity
"""

import matplotlib.pyplot as plt
import seaborn as sns

# Scatter plot of the independent variable vs dependent variable
sns.pairplot(df, x_vars=['GRE Score', 'TOEFL Score', 'University Rating', 'CGPA'], y_vars=['Chance of Admit '], height=3)
plt.show()

"""4.Test for Homoscedasticity"""

import matplotlib.pyplot as plt
import seaborn as sns

# Assuming the model is fitted and we have y_pred as predicted values
  # Predicted values
residuals = y_train - results.predict(X_sm)  # Residuals

# Plot residuals vs predicted values
plt.scatter(results.predict(X_sm), residuals)
plt.axhline(y=0, color='r', linestyle='--')  # Line at 0 for reference
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted Values Plot')
plt.show()

"""No funnel shape, distributed constantly mostly, we can say no heteroscedasticity

5.Normality of residuals
"""

import matplotlib.pyplot as plt

# Assuming residuals are calculated already
residuals = y_train - results.predict(X_sm)

# Plot the histogram of residuals
plt.hist(residuals, bins=30, edgecolor='black')
plt.title('Histogram of Residuals')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.show()

"""the residuals are seems to be left-skewed"""

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Predict on both train and test data
y_train_pred = results.predict(sm.add_constant(X_train))
y_test_pred = results.predict(sm.add_constant(X_test))

# Calculate MAE, RMSE, R², and Adjusted R² for both train and test sets
def adjusted_r2(r2, n, k):
    return 1 - ((1 - r2) * (n - 1) / (n - k - 1))

# Number of samples and features
n_train, k_train = X_train.shape
n_test, k_test = X_test.shape

# Training Performance
train_mae = mean_absolute_error(y_train, y_train_pred)
train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
train_r2 = r2_score(y_train, y_train_pred)
train_adj_r2 = adjusted_r2(train_r2, n_train, k_train)

# Testing Performance
test_mae = mean_absolute_error(y_test, y_test_pred)
test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
test_r2 = r2_score(y_test, y_test_pred)
test_adj_r2 = adjusted_r2(test_r2, n_test, k_test)

# Print Results
print(f"Train MAE: {train_mae:.4f}, Test MAE: {test_mae:.4f}")
print(f"Train RMSE: {train_rmse:.4f}, Test RMSE: {test_rmse:.4f}")
print(f"Train R²: {train_r2:.4f}, Test R²: {test_r2:.4f}")
print(f"Train Adjusted R²: {train_adj_r2:.4f}, Test Adjusted R²: {test_adj_r2:.4f}")

"""The Trainning and test data , almost gives the similar, results as expected, without any overfitting and underfiting.

**Recommendations**

Students , who wanna get a chance of admit, should mainly focus on their CGPA of college, and then they should concentrate on TOFEL and GRE scores.
"""