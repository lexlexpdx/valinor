# %% [markdown]
# Lex Albrandt  
# CS445  
# HW 1

# %% [markdown]
# ## Question 1:  
#  
# 1a)  
# A target variable the retailer could use would be the future sales of a product  
#   
# 1b)  
#   
# For this linear regression the numeric score would be a feature as well as each of the  
# judgement words (we would tokenize these). So the feature vector would consist of the numeric score  
# and all other tokens.  
# The model could be written as:   
#   
# $\begin{align}
# y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + ... + \beta_n x_n
# \end{align}$  
#   
# 1c)  
#    
# I think that you could reduce the number of features by using either the numeric values  
# or the token words, and not both, since they likely correlate  
#   
# 1d)  
#   
# Because the numeric scores are on different scales, you could use feature scaling, either  
# using min/max scaling or standardization to ensure that all your features use the same scale.

# %% [markdown]
# ## Question 2:
#  
# 2a)  
#   
# The categorical data in this dataset is type, color, and size  
#   
# 2b)  
#   
# There would be 8 variables after one-hot coding: banana, apple, red, green, yellow, small,    
# large, and price.  

# %% [markdown]
# ## Question 3  
#  
# 3a)  
# The feature matrix A would be:  
#   
# $\begin{align}
# A = \begin{bmatrix}
# 1 & 1400 & 3\\
# 1 & 1600 & 3\\
# 1 & 1700 & 4\end{bmatrix}
# \end{align}$  
#   
# 3b)  
#   
# The target variable vector y would be:  
#   
# $\begin{align}
# y = \begin{bmatrix}
# 245\\
# 312\\
# 279\end{bmatrix}
# \end{align}$  
#   
# 3c)  
#   
# To compute the coefficients and find the coefficient matrix we use:  
# $\begin{align}
# \beta = (A^T A)^{-1} A^T y
# \end{align}$  
#   
# We begin by finding $A^T$:   
#   
# $\begin{align}
# A^T = \begin{bmatrix}
# 1 & 1 & 1\\
# 1400 & 1600 & 1700\\
# 3 & 3 & 4\end{bmatrix}
# \end{align}$  
#   
# Next we will calculate $A^T A$:  
#   
# $A^T A = \begin{bmatrix}
# 1 & 1 & 1\\
# 1400 & 1600 & 1700\\
# 3 & 3 & 4
# \end{bmatrix}
# \begin{bmatrix}
# 1 & 1400 & 3\\
# 1 & 1600 & 3\\
# 1 & 1700 & 4
# \end{bmatrix}
# = \begin{bmatrix}
# 3 & 4700 & 10\\
# 4700 & 7410000 & 15800\\
# 10 & 15800 & 34
# \end{bmatrix}$  
#   
# We then find the inverse $(A^T A)^{-1}$:  
#   
# $(A^T A)^{-1} = 
# \begin{bmatrix}
# 57.5 & -0.045 & 4.00\\
# -0.045 & 0.00005 & -0.01\\
# 4.00 & -0.01 & 3.50
# \end{bmatrix}$  
#   
# Next we find $A^T y$:
#   
# $A^T y = \begin{bmatrix}
# 1 & 1 & 1\\
# 1400 & 1600 & 1700\\
# 3 & 3 & 4
# \end{bmatrix}
# \begin{bmatrix}
# 245\\
# 312\\
# 279
# \end{bmatrix} = 
# \begin{bmatrix}
# 836\\
# 1316500\\
# 2787
# \end{bmatrix}$  
#   
# Finally, we calculate $\beta$:
#   
# $\beta = (A^T A)^{-1} A^T y = \begin{bmatrix}
# -24.5\\
# 0.335\\
# -66.5
# \end{bmatrix}$  
#   
# 3d)  
#   
# To find the predicted price of a house with a size of 1500 sqft and 3 bedrooms  
# We use the following equation: 
#   
# $Price = -24.5 + 0.335 \times 1500 + -66.5 \times 3 = 278.5$  
#   
# So the predicted price is $278500.
#   

# %% [markdown]
# ## Question 4  
#   
# We want to show that $A^T A$ is invertible iff the columns of $A$ are linearly  
# independent.  
# We know that if $A^T A$ is invertible, then $Rank(A^T A)=n$  
# We also know that if $A$ is a matrix with real numbers, then $Rank(A^T A)=Rank(A)$  
# If the $Rank(A)=n$, then the matrix is full rank, which means that all of its rows  
# are linearly indepdent.  
#   
# Thus:  
#   
# $A^T A \text{is invertible} \iff Rank(A^T A)=Rank(A) \iff Rank(A)=n \iff \text{columns of A are linearly independent}$
#   

# %% [markdown]
# ## Question 5  
#   
# 5a)  
#   
# The 8 attributes in the dataset are:  
#
# - MedInc
# - HouseAge
# - AveRooms
# - AveBedrms
# - Population
# - AveOccup
# - Latitude
# - Longitude  

# %%
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from sklearn.datasets import fetch_california_housing
california = fetch_california_housing()
X = california.data
y = california.target

print("Question 5b:\n")
df = pd.DataFrame(X, columns = california.feature_names)
print(df.loc[10:15, ['HouseAge', 'AveRooms', 'Population']])

# Isolate only average occupancy
X_aveocc = X[:, california.feature_names.index('AveOccup')]

# Split test data
split_index = int(len(X_aveocc) * (2 / 3))
X_train = X_aveocc[:split_index]
X_test = X_aveocc[split_index:]
y_train = y[:split_index]
y_test = y[split_index:]

ym = np.mean(y_train)
xm = np.mean(X_train)
syy = np.mean((y_train - ym) ** 2)
syx = np.mean((y_train - ym) * (X_train - xm))
sxx = np.mean((X_train - xm) ** 2)
beta1 = syx / sxx
beta0 = ym - beta1 * xm 

print(f"\nQuestion 5c:")
print(f"Beta1 (slope): {beta1:.4f}")
print(f"Beta0 (intercep): {beta0:.4f}")

y_hat_tst = beta0 + beta1 * X_test
y_hat_tr = beta0 + beta1 * X_train

train_MSE = np.mean((y_train - y_hat_tr) ** 2)
test_MSE = np.mean((y_test - y_hat_tst) ** 2)

print(f"Training MSE: {train_MSE:.4f}")
print(f"Test MSE = {test_MSE:.4f} \n")

print(f"Question 5d: \n")

R2_train = 1 - np.sum((y_train - y_hat_tr) ** 2) / np.sum((y_train - np.mean(y_train)) ** 2)
R2_test = 1 - np.sum((y_test - y_hat_tst) ** 2) / np.sum((y_test - np.mean(y_test)) ** 2)

print(f"Training R^2: {R2_train}")
print(f"Test R^2: {R2_test}")

# %% [markdown]
# Because the training and test $R^2$ values are close to zero or negative, Average Occupancy is a 
# poor predictor of the median house value  
#   
# ## Question 6  
#   
# 6a)  
#   
#
# if $Ax=b$ has no solution, then $b \notin col(A)$ and $Rank(A) \lt m$  
#   
# 6b)  
#   
# if $Ax=b$ has exactly 1 solution then $Rank(A)=n$ and $b \in col(A)$  
#   
# 6c)  
#   
# if $Ax=b$ has infinitely many solutions then $b \in col(A)$ and $Rank(A) \lt n$
