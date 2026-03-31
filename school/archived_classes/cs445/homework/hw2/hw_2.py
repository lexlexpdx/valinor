# %% [markdown]
# Lex Albrandt  
# CS445  
# HW 2  

# %%
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso

# %% [markdown]
# ## Question 1 
#   
# ## 1a)  
#   

# %%
# variable for storing CV MSE values for output later
cv_mse_results = []

# set up for reproducibility
np.random.seed(42)

# 100 samples
n = 100
x_train = np.random.uniform(-5, 5, n)

# for polynomial y = 2 + 0.5x - 0.1x^2
beta = np.array([2, 0.5, -.1])

# Add Gaussian noise
epsilon = np.random.normal(0, 1, n)

# define polynomial
# Expects coefficients from lowest order to highest order
y_true_train = poly.polyval(x_train, beta)
y_train = y_true_train + epsilon

# Plot the data
plt.title("Synthetic data from noisy quadratic model")
plt.scatter(x_train, y_train)
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()


# %% [markdown]
# ## 1b) and 1c) and 1d)
#   
# ### Linear Model  
#   

# %%
d = 1
beta_hat = poly.polyfit(x_train, y_train, d)

x_true = np.linspace(-5, 5, 100)
y_true = poly.polyval(x_true, beta)
y_true_hat = poly.polyval(x_true, beta_hat)
plt.plot(x_true, y_true, 'r', linewidth = 2)
plt.plot(x_true, y_true_hat, 'g', linewidth = 2)

# Plot scatter plot of generated data
plt.title("True Order vs Attempted Linear Fit")
plt.scatter(x_train, y_train)
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend(['True (dtrue = 2)', 'Est (d = 1)' 'Data'], loc = 'upper left')
plt.show()



# %% [markdown]
# We see that a regression model with a degree of 1 does not fit this data  
#   
# Now we will compute training MSE for $d=1$  
#   

# %%
y_hat_train = poly.polyval(x_train, beta_hat)
mse = np.mean((y_train - y_hat_train) ** 2)
print(f"Training MSE: {mse:.4f}")

# %% [markdown]
# We can see that with $d=1$ the MSE is greater than 1, indicating that a linear  
# model is a poor fit for our data.  
#   
# Next we will compute a 5-fold cross-validation for unseen data  
#   

# %%
# Number of folds
K = 5
d = 1

# Shuffle indices (100 data points)
indices = np.random.permutation(n)
folds = np.array_split(indices, K)

mse_folds = []

for k in range(K):

    # Validation indices
    val_index = folds[k]

    # Training indices
    # Takes all indices up to k, and all indices after k and stacks them
    # into a 1D array
    train_index = np.hstack(folds[:k] + folds[k + 1:])

    # Split data
    x_tr = x_train[train_index]
    y_tr = y_train[train_index]
    x_val = x_train[val_index]
    y_val = y_train[val_index]

    # Fit the model on the training fold
    beta_hat = poly.polyfit(x_tr, y_tr, d)

    # Predict on validation fold
    y_val_hat = poly.polyval(x_val, beta_hat)

    # Compute MSE for this fold
    mse = np.mean((y_val - y_val_hat) ** 2)
    mse_folds.append(mse)

# Cross-Validated MSE
cv_mse = np.mean(mse_folds)
cv_mse_results.append((d, cv_mse))
print(f"5-fold CV MSE for d = 1: {cv_mse:.4f}")
    


# %% [markdown]
# ### Quadratic Model  
#   
# %%
d = 2
beta_hat = poly.polyfit(x_train, y_train, d)

x_true = np.linspace(-5, 5, 100)
y_true = poly.polyval(x_true, beta)
y_true_hat = poly.polyval(x_true, beta_hat)
plt.plot(x_true, y_true, 'r', linewidth = 2)
plt.plot(x_true, y_true_hat, 'g', linewidth = 2)

# Plot scatter plot of generated data
plt.title("True Order vs Attempted Quadratic Fit")
plt.scatter(x_train, y_train)
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend(['True (dtrue = 2)', 'Est (d = 2)', 'Data'], loc = 'upper left')
plt.show()

# %% [markdown]
# It appears here that a quadratic model is a good fit. We will attempt a cubic  
# model to ensure that quadratic is, in fact, the proper fit.  
#   
# Now we will compute training MSE for $d=2$  
#    

# %%
y_hat_train = poly.polyval(x_train, beta_hat)
mse = np.mean((y_train - y_hat_train) ** 2)
print(f"Training MSE: {mse:.4f}")

# %% [markdown]
# The training MSE here is pretty good, indicating this model order is likely a  
# good fit.  
#   
# Next we will calculate the 5-fold Cross-Validation MSE for unseen data  
#  

# %%
K = 5
d = 2

indices = np.random.permutation(n)
folds = np.array_split(indices, K)

mse_folds = []

for k in range(K):
    val_index = folds[k]

    train_index = np.hstack(folds[:k] + folds[k + 1:])

    x_tr = x_train[train_index]
    y_tr = y_train[train_index]
    x_val = x_train[val_index]
    y_val = y_train[val_index]

    beta_hat = poly.polyfit(x_tr, y_tr, d)

    y_val_hat = poly.polyval(x_val, beta_hat)
    
    mse = np.mean((y_val - y_val_hat) ** 2) 
    mse_folds.append(mse)

cv_mse = np.mean(mse_folds)
cv_mse_results.append((d, cv_mse))
print(f"5-fold CV MSE for d = 2: {cv_mse:.4f}")


# %% [markdown]
# ### Cubic Model  
#   
# %%
d = 3
beta_hat = poly.polyfit(x_train, y_train, d)

x_true = np.linspace(-5, 5, 100)
y_true = poly.polyval(x_true, beta)
y_true_hat = poly.polyval(x_true, beta_hat)
plt.plot(x_true, y_true, 'r', linewidth = 2)
plt.plot(x_true, y_true_hat, 'g', linewidth = 2)

# Plot scatter plot of generated data
plt.title("True Order vs Attempted Cubic Fit")
plt.scatter(x_train, y_train)
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend(['True (dtrue = 2)', 'Est (d = 3)', 'Data'], loc = 'upper left')
plt.show()
# %% [markdown]
# It is difficult to tell from this graph if cubic is a better fit, which points out  
# a flaw of trying to "eyeball" the fit: our estimation may not be mathematically sound  
#  
# Let's compute the training MSE for $d=3$  
#   
# %%
y_hat_train = poly.polyval(x_train, beta_hat)
mse = np.mean((y_train - y_hat_train) ** 2)
print(f"Training MSE: {mse:.4f}")

# %% [markdown]
# We can see that the MSE is slightly farther away from 1 than for $d=2$, but appears  
# to be a decent fit. We will now compute the CV MSE for this model order.  
#  

# %%
K = 5
d = 3

mse_folds = []

for k in range(K):
    
    val_index = folds[k]

    train_index = np.hstack(folds[:k] + folds[k + 1:])

    x_tr = x_train[train_index]
    y_tr = y_train[train_index]
    x_val = x_train[val_index]
    y_val = y_train[val_index]

    beta_hat = poly.polyfit(x_tr, y_tr, d)

    y_val_hat = poly.polyval(x_val, beta_hat)

    mse = np.mean((y_val - y_val_hat) ** 2)
    mse_folds.append(mse)

cv_mse = np.mean(mse_folds)
cv_mse_results.append((d, cv_mse))
print(f"5-fold CV MSE for d = 3: {cv_mse:.4f}")

# %% [markdown]
# ### Model order 10   
#   

# %%
d = 10
beta_hat = poly.polyfit(x_train, y_train, d)

x_true = np.linspace(-5, 5, 100)
y_true = poly.polyval(x_true, beta)
y_true_hat = poly.polyval(x_true, beta_hat)
plt.plot(x_true, y_true, 'r', linewidth = 2)
plt.plot(x_true, y_true_hat, 'g', linewidth = 2)

# Plot scatter plot of generated data
plt.title("True Order vs Order of degree 10")
plt.scatter(x_train, y_train)
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend(['True (dtrue = 2)', 'Est (d = 10)', 'Data'], loc = 'upper left')
plt.show()
# %% [markdown]
# In this example we see that a model degree of 10 clearly overfits the data and does  
# not generalize properly.  
#   
# Now we will calculate training MSE for $d=10$  
#   

# %%
y_hat_train = poly.polyval(x_train, beta_hat)
mse = np.mean((y_train - y_hat_train) ** 2)
print(f"Training MSE: {mse:.4f}")

# %% [markdown]
# We can see that the training MSE for $d=10$ indicates this model order is beginning to  
# overfit the data. Let's calculate the CV MSE for $d=10$  
#  

# %%
K = 5
d = 10

mse_folds = []

for k in range(K):

    val_index = folds[k]
    train_index = np.hstack(folds[:k] + folds[k + 1:])

    x_tr = x_train[train_index]
    y_tr = y_train[train_index]
    x_val = x_train[val_index]
    y_val = y_train[val_index]

    beta_hat = poly.polyfit(x_tr, y_tr, d)

    y_val_hat = poly.polyval(x_val, beta_hat)

    mse = np.mean((y_val - y_val_hat) ** 2)
    mse_folds.append(mse)

cv_mse = np.mean(mse_folds)
cv_mse_results.append((d, cv_mse))
print(f"5-fold CV MSE for d = 10: {cv_mse:.4f}")

# %% [markdown]
# Our results from the 5-fold CV MSE for $d=10$ once again show  
# that this model is beginning to overfit the data.  
#   
# ## 1e)  
#   
# Below we will compare the CV MSE values for each of the models to  
# determine which model has the best generalization performance.  

# %%
sorted_cvmse = sorted(cv_mse_results, key = lambda x: x[1])
headers = ["Model Order", "CV MSE"]
cell_text = [[d, f"{mse:.4f}"] for d, mse in sorted_cvmse]

fig, ax = plt.subplots(figsize = (5, 2))
ax.axis("off")

table = ax.table(cellText = cell_text, colLabels = headers, loc = 'center', cellLoc = "center")
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1.2, 1.2)

for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_text_props(weight = "bold")

plt.title("Model Order vs CV MSE")
plt.show()

# %% [markdown]
# Based on the above table we can see that the model with order $d=2$  
# showed the best generalization  
#   
# ## 1f)  
#   
# Higher-order models are able to achieve lower training error because  
# they can fit the actual signal and any noise in the training data, but  
# when they see new data, the error is higher because they have high variance  
# and are overfitting the data.  
#  
# ## 1g)  
# The value of irreducible error is the vairance of the noise term and cannot  
# be reduced by model choice. In our example the irreducible error is 1 because  
# the noise term has a variance of 1.

# %% [markdown]
# # Question 2  
#   
# ## 2a)  
#   
# Given the following equation:  
# $\hat\beta=(A^TA)^{-1}A^Ty$  
#   
# We want to prove that if the columns of $A$ are linearly dependent, then  
# $A^TA$ is not invertible.  
#   
# Assume that the columns of $A\in\mathbb{R}^{n \times p}$ are linearly dependent.
# By **Hint 1**, there exists a nonzero vector $c\in\mathbb{R}^p$ such that  
#   
# $$Ac=0$$  
#   
# Now consider the matrix $A^TA\in\mathbb{p \times p}$. Then:  
#   
# $$A^TAc=A^T(Ac)=A^T0=0$$  
#   
# Thus, there exists a **nonzero** vector $c$ such that  
#   
# $$A^TAc=0$$  
# By **Hint 2**, a  square matrix is invertible if and only if the solution to  
# $Zc=0$ is $c=0$. Since $A^T
# A$ has a nontrivial null vector, it follows that  
# $A^TA$ is **not invertible**.  
#   
# Therefore, if the columns of $A^TA$ are linearly dependent, then $A^TA$ is  
# not invertible.  
#  
# ## 2b)  
#   
# The modified estimator for Ridge regression is as follows:  
#   
# $$\hat{\beta}_{\text{ridge}}=(A^TA+{\alpha}I)^{-1}A^Ty, \ \alpha>0$$
#   
# As shown in the previous question, when the columns of $A^TA$ are linearly dependent  
# then $A^TA$ is not invertible, even if $A^TA$ is singular. By adding ${\alpha}I$ where 
# $\alpha>0$, the matrix $(A^TA+{\alpha}I)$ positive definite, which ensures there is a   
# unique solution to the modified estimator.  
#   

# %% [markdown]
# # Question 3  
#   
# To split a dataset into training and test sets we first shuffle the data so that  
# any existing patterns are broken up. Then we choose a split ratio, this is selected  
# based on the problem at hand. Then we divide the dataset into training data and testing  
# data based on the split ratio. Because we are taking a portion of the data that was unseen  
# in testing, and evaluating the model on that, we avoid overfitting, and increases generalization.  
#   
# # Question 4  
#   

# %%
# Import california housing dataset
from sklearn.datasets import fetch_california_housing

california = fetch_california_housing()
X = california.data
y = california.target

# %% [markdown]
# ## 4a) and 4b)
#   

# %%
# Create scalar object for feature matrix
xscal = StandardScaler()

# Fit and transform the feature matrix
X_scaled = xscal.fit_transform(X)

# Print first 5 rows of original and scaled data for comparison

# convert to DataFrame first for better output
X_df = pd.DataFrame(X, columns = california.feature_names)
X_df.head()

# %%
X_scaled_df = pd.DataFrame(X_scaled, columns = california.feature_names)
X_scaled_df.head()

# %% [markdown]
# ## 4c)  
#   

# %%
def lasso_reg(alpha_vals):
    
    # split training and test data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y,
        test_size = 0.2,
        random_state = 42
    )

    # Fit and transform y and X_test
    yscal = StandardScaler()
    y_train_scal = yscal.fit_transform(y_train[:,None])
    y_test_scal = yscal.transform(y_test[:,None])

    mse_list = []

    for alpha in alpha_vals:
       
       # Fit on the training data
       reg = Lasso(alpha = alpha, random_state = 42, max_iter = 10000) 
       reg.fit(X_train, y_train_scal.ravel())

       # Score on the test data
       y_pred = reg.predict(X_test)
       mse = np.mean((y_test_scal - y_pred) ** 2) 
       mse_list.append(mse)

    return mse_list
    
alpha_values = np.logspace(-6, -1, 10)
mse_results = lasso_reg(alpha_values)

results_df = pd.DataFrame({
    "Alpha": alpha_values,
    "MSE": mse_results
})

results_df = results_df.round({"Alpha": 6, "MSE": 4})
print(results_df)
# %% [markdown]
# ## 4d)  
#   

# %%
alpha_values = np.logspace(-4, -1, 10)
mse_results = lasso_reg(alpha_values)

results_df = pd.DataFrame({
    "Alpha": alpha_values,
    "MSE": mse_results
})

results_df = results_df.round({"Alpha": 6, "MSE": 4})
print(results_df)
