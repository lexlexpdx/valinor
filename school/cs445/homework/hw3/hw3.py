# %% [markdown]
# Lex Albrandt  
# CS 445
# HW 3  
#   
# # Question 1  
#   
# ## 1a)  
#   

# %%
# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
x1 = np.array([3, 5, 7, 8, 10])
x2 = np.array([0, 1, 1, 2, 1])
y = np.array([0, 1, 0, 1, 1])

mask0 = (y == 0)
mask1 = (y == 1)

plt.figure()
plt.scatter(x1[mask0], x2[mask0], marker = 'o', label = 'y = 0')
plt.scatter(x1[mask1], x2[mask1], marker = 'x', label = 'y = 1')
plt.xlabel('Income (x1 tens of thousands $)')
plt.ylabel('Number of websites x2')
plt.legend()
plt.grid(True, alpha = 0.3)
plt.show()

