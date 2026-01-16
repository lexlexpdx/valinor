# %% [markdown]
# Lex Albrandt  
# CS445  
# HW 1

# %% [markdown]
# ## Question 1:  
#  
# 1a)<br>
# A target variable the retailer could use would be the future sales of a product
# <br><br>
# 1b)<br>
# For this linear regression the numeric score would be a feature as well as each of the  
# judgement words (we would tokenize these). So the feature vector would consist of the numeric score  
# and all other tokens.  
# The model could be written as:   
# <br>
# $\begin{align}
# y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + ... + \beta_n x_n
# \end{align}$  
# <br>
# 1c)<br>
# I think that you could reduce the number of features by using either the numeric values  
# or the token words, and not both, since they likely correlate  
# <br>
# 1d)<br>
# Because the numeric scores are on different scales, you could use feature scaling, either  
# using min/max scaling or standardization to ensure that all your features use the same scale.

# %% [markdown]
# ## Question 2:
#  
# 2a)<br>
# The categorical data in this dataset is type, color, and size  
# <br>
# 2b)<br>
# There would be 8 variables after one-hot coding: banana, apple, red, green, yellow, small,    
# large, and price.  

# %% [markdown]
# ## Question 3  
#  
# 3a)<br>
# The feature matrix A would be:  
# <br>
# $\begin{align}
# A = \begin{bmatrix}
# 1 & 1400 & 3\\
# 1 & 1600 & 3\\
# 1 & 1700 & 4\end{bmatrix}
# \end{align}$
# <br><br>
# 3b)<br>
# The target variable vector y would be:  
# <br>
# $\begin{align}
# y = \begin{bmatrix}
# 245\\
# 312\\
# 279\end{bmatrix}
# \end{align}$  
# <br>
# 3c)<br>
# To compute the coefficients and find the coefficient matrix we use:  
# $\begin{align}
# \beta = (A^T A)^{-1} A^T y
# \end{align}$  
# <br>
# We begin by finding $A^T$:   
# <br>
# $\begin{align}
# A^T = \begin{bmatrix}
# 1 & 1 & 1\\
# 1400 & 1600 & 1700\\
# 3 & 3 & 4\end{bmatrix}
# \end{align}$
# <br><br>
# Next we will calculate $A^T A$:  
# <br>
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
# <br><br>
# We then find the inverse $(A^T A)^{-1}$:  
# <br>
# $(A^T A)^{-1} = 
# \begin{bmatrix}
# 57.5 & -0.045 & 4.00\\
# -0.045 & 0.00005 & -0.01\\
# 4.00 & -0.01 & 3.50
# \end{bmatrix}$  
# <br>
# Next we find $A^T y$:
# <br>
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
# <br><br>
# Finally, we calculate $\beta$:
# <br>
# $\beta = (A^T A)^{-1} A^T y = \begin{bmatrix}
# -24.5\\
# 0.335\\
# -66.5
# \end{bmatrix}$  
# <br>
# 3d)<br>
# <br>
# To find the predicted price of a house with a size of 1500 sqft and 3 bedrooms  
# We use the following equation: 
# <br><br>
# $Price = -24.5 + 0.335 \times 1500 + -66.5 \times 3 = 278.5$  
# <br>
# So the predicted price is $278500.
