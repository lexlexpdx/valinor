# %% [markdown]
# Lex Albrandt  
# CS445  
# HW 2  

# %%
import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly

# %% [markdown]
# ## Question 1 
#   
# 1a)  
#   

# %%
# set up for reproducibility
np.random.seed(42)

# 100 samples
n = 100
xdat = np.random.uniform(-5, 5, n)

# for polynomial y = 2 + 0.5x - 0.1x^2
beta = np.array([2, 0.5, -.1])

# Add Gaussian noise
epsilon = np.random.normal(0, 1, n)

# define polynomial
# Expects coefficients from lowest order to highest order
y0 = poly.polyval(xdat, beta)
ydat = y0 + epsilon

# Plot the data
plt.title("Synthetic data from noisy quadratic model")
plt.scatter(xdat, ydat)
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()


# %% [markdown]
# 1b) and 1c)  
#   

# %%
d = 1
beta_hat = poly.polyfit(xdat, ydat, d)

x_true = np.linspace(-5, 5, 100)
y_true = poly.polyval(x_true, beta)
y_true_hat = poly.polyval(x_true, beta_hat)
plt.plot(x_true, y_true, 'r', linewidth = 2)
plt.plot(x_true, y_true_hat, 'g', linewidth = 2)

# Plot scatter plot of generated data
plt.title("True Order vs Attempted Linear Fit")
plt.scatter(xdat, ydat)
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend(['True (dtrue = 2)', 'Est (d = 1)' 'Data'], loc = 'upper left')
plt.show()



# %% [markdown]
# We see that a regression model with a degree of 1 does not fit this data  

# %%
d = 2
beta_hat = poly.polyfit(xdat, ydat, d)

x_true = np.linspace(-5, 5, 100)
y_true = poly.polyval(x_true, beta)
y_true_hat = poly.polyval(x_true, beta_hat)
plt.plot(x_true, y_true, 'r', linewidth = 2)
plt.plot(x_true, y_true_hat, 'g', linewidth = 2)

# Plot scatter plot of generated data
plt.title("True Order vs Attempted Quadratic Fit")
plt.scatter(xdat, ydat)
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend(['True (dtrue = 2)', 'Est (d = 2)', 'Data'], loc = 'upper left')
plt.show()

# %% [markdown]
# It appears here that a quadratic model is a good fit. We will attempt a cubic  
# model to ensure that quadratic is, in fact, the proper fit.  

# %%
d = 3
beta_hat = poly.polyfit(xdat, ydat, d)

x_true = np.linspace(-5, 5, 100)
y_true = poly.polyval(x_true, beta)
y_true_hat = poly.polyval(x_true, beta_hat)
plt.plot(x_true, y_true, 'r', linewidth = 2)
plt.plot(x_true, y_true_hat, 'g', linewidth = 2)

# Plot scatter plot of generated data
plt.title("True Order vs Attempted Cubic Fit")
plt.scatter(xdat, ydat)
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend(['True (dtrue = 2)', 'Est (d = 3)', 'Data'], loc = 'upper left')
plt.show()
# %% [markdown]
# It is difficult to tell from this graph if cubic is a better fit, which points out  
# a flaw of trying to "eyeball" the fit: our estimation may not be mathematically sound  

# %%
d = 10
beta_hat = poly.polyfit(xdat, ydat, d)

x_true = np.linspace(-5, 5, 100)
y_true = poly.polyval(x_true, beta)
y_true_hat = poly.polyval(x_true, beta_hat)
plt.plot(x_true, y_true, 'r', linewidth = 2)
plt.plot(x_true, y_true_hat, 'g', linewidth = 2)

# Plot scatter plot of generated data
plt.title("True Order vs Order of degree 10")
plt.scatter(xdat, ydat)
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend(['True (dtrue = 2)', 'Est (d = 10)', 'Data'], loc = 'upper left')
plt.show()
# %% [markdown]
# In this example we see that a model degree of 10 clearly overfits the data and does  
# not generalize properly.
