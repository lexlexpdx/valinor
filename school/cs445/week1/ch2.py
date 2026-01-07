# Auto example from class

# Load libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# Load data
# -------------------------

# Note: df = dataframe, how we will initially load data
# We need more info to show correctly
#df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data')

# establish column names, store in a list object
names = ['MPG', 'Cylinders', 'Displacement', 'Horsepower', 'Weight',
         'Acceleration', 'Model Year', 'Origin', 'Car Name']

# Note: delim_whitepsace is depreciated, use sep=r'\s+'
#df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data',
               #  header = None, names = names, delim_whitespace = True, na_values = '?')
df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data',
                 header = None, names = names, sep = r'\s+', na_values = '?')
                

# When running in terminal you have to use a print statement, jupyter shows this nicely
#print(df.head(6))

# See the shape of a dataframe object using df.shape
#print(df.shape)

# See the column names with df.columns
#print(df.columns)

# To see the index, use df.index
#print(df.index)

# For other specific functionality, see the CH2 code

# --------------------------------
# Plotting the data
# --------------------------------

# Import the matplotlib library (see top)

# Note: we must convert the dataframe to a numpy array

# convert. This shows two different ways of extracting the columns you want to use. A string object would be useful
# for long names.
xstr = 'Displacement'
x = np.array(df[xstr])
y = np.array(df['MPG'])

# Creating a scatter plot for the data

# plt.plot(x axis, y axis, fmt)
plt.plot(x, y, 'bo')
plt.xlabel(xstr)
plt.ylabel('MPG')
plt.grid(True)

# in python code, unlike jupyter notebooks, you must use plt.show() to actually show the plot!
plt.show()

# -----------------------------
# Manipulating arrays
# -----------------------------

# Sample mean
# Note: just use regular f-string formatting here, it's different in jupyter notebooks
mx = np.mean(x)
my = np.mean(y)
print(f"Mean {xstr} = {mx:.1f}, mean mpg = {my:.1f}")

# # Mean of all cars with mpg less than 25
# my_lt25 = np.mean(y < 25)
# print(f"Mean for cars with mpg < 25 = {my_lt25:.1f}")

# Mean of all cars with mpg greater than 25
my_gt25 = np.mean(y > 25)
print(f"Mean for cars with mpg > 25 = {my_gt25:.7f}")

# This creates a boolean array that gives a true value if the mpg is > 25, false otherwise
gt25_mask = (y > 25)
print(f"Cars with MPG > 25: {np.sum(gt25_mask)} out of {len(y)} cars.")

# if we want to find the mean displacement for cars that have mpg > 25 we can do it a couple of ways
# This is displacement for a subset of cars
# Here np.mean(x * gt25_mask) gives us the mean number of cars with mpg > 25, it multiplies all x values by the boolean mask
# That number is then divided by the mean number of cars
print(f"Average displacement: {np.mean(x * gt25_mask) / np.mean(gt25_mask)}")

# Another way to do this is:
print(f"Average displacement: {np.mean(x[gt25_mask])}")

# ---------------------------------
# Plotting functions
# ---------------------------------

