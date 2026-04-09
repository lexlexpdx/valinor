# %% [markdown]
# Lex Albrandt  
# SYSC410  
# Data Adventure 1  

# %%
# Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.impute import SimpleImputer

# %% [markdown]
# # Step 1: Data loading, inspection, and cleaning
#   
# The first step in our ML pipeline is loading the csv file using the `pandas` library. 
# We will also output the first 5 rows of data to inspect. 

# %%
df = pd.read_csv('../data/skyserver_classroom.csv')
print(df.head())
print(f"\nData Rows and Columns: {df.shape}")

# %% [markdown]
# From the output above we can see that our dataset has 1500 rows and 13 columns. 
# The columns of our data are as follows:  
# - ID
#   - Object ID
# - Class
#    - Object Class
# - Redshift
#   - Measures how much light from an object has been stretched due to the 
# expansion of the universe
# - mag_u
#   - Ultraviolet wavelength magnitude
# - mag_g
#   - Green wavelength magnitude
# - mag_r
#   - Red wavelength magnitude
# - mag_i
#   - Near-infrared wavelength magnitude
# - mag_z
#   - Infrared wavelength magnitude
# - ra
#   - Right Ascension: horizontal position in degrees
# - dec
#   - Declination: vertical position in degrees
# - u_g
#   - $\text{u\_g} = \text{mag\_u} - \text{mag\_g}$
#   - Color index between $u$ and $g$ bands
# - g_r
#   - $\text{g\_r} = \text{mag\_g} - \text{mag\_r}$
#   - Color index between $g$ and $r$ bands
# - r_i
#   - $\text{r\_i} = \text{mag\_r} - \text{mag\_i}$
#   - Color index between $r$ and $i$ bands
# - i_z
#   - $\text{i\_z} = \text{mag\_i} - \text{mag\_z}$
#   - Color index between $i$ and $z$ bands
#   
# There are also 3 classes in this dataset: Star, Galaxy, and QSO (quasar).  
#
# Now we want to check for missing values.

# %%
missing_count = df.isna().sum()
print(missing_count)

# %% [markdown]
# Based on the output above there are no missing values in the dataset. However, 
# we will also use the `SimpleImputer` method from `sklearn` to impute any missing 
# values.

# %%
numeric_cols = ["ra", 
                "mag_u", 
                "mag_g", 
                "mag_r", 
                "mag_i", 
                "mag_z", 
                "dec", 
                "redshift", 
                "u_g", 
                "g_r", 
                "r_i", 
                "i_z"]

imputer = SimpleImputer(strategy = "median")
df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
df = df.dropna()
print(f"Rows after imputation and cleanup: {len(df)}")

# %% [markdown]
# # Step 2: Deeper EDA  
#   
# ## Correlation matrix  
# We can use a correlation matrix to see which features are most related to redshift.

# %%
corr = df[numeric_cols].corr()
plt.figure(figsize = (8, 8))
sns.heatmap(corr, annot = True, fmt = "0.2f", cmap = "RdBu_r", center = 0, square = True)
plt.title("Feature correlation matrix")
plt.show()

# Convert to a panda series and print
corr_redshift = (
    df[numeric_cols]
    .corr()["redshift"]
    .drop("redshift")
    .sort_values(key = abs, ascending = False)
)
print(corr_redshift)

# %% [markdown]
# From the heatmap and panda series above ,we can see that `mag_z` and `mag_i` are 
# most closely correlated to `redshift`. We also want to look at some distribution 
# plots for our `redishift`.  
#   

# %%
fig, axes = plt.subplots(1, 2, figsize = (10, 4))
sns.histplot(data = df, x = "redshift", kde = True, ax = axes[0])
axes[0].set_title("Redshift Distribution")

sns.boxplot(data = df, x = "class", y = "redshift", ax = axes[1])
plt.show()
