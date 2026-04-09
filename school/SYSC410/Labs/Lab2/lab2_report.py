# %% [markdown]
# Lex Albrandt  
# SYSC410  
# Lab 2 Report  
#   
# # Pipeline A  
#   
# ## Distributions  
#  
# When cycling through each of the distributions there did not appear to be any 
# immediately obvious outliers. Below are examples of `bill_len_mm` and `bill_depth_mm` 
# distributions by species:  
#   
# ![bill length distribution](./bill_len_distro.png)   
#   
# ![bill depth distribution](./bill_depth_distro.png)   
#  
# We can see in each of the distributions there is a significant overlap in species. 
# Later in the lab we will use feature engineering to create a new feature that 
# helps separate the species.  
#   
# ## Scatter Plot
#  
# In this section we will look at scatter plots for the features pairs in our dataset. 
# There are two sets of pairs that stood out: bill length vs bill depth, and bill length 
# vs body mass, as seen in the screenshots below:  
#   
# ![Scatter 1](./bill_depth_bill_len_scat.png)   
#   
# ![Scatter 2](./bill_len_body_mass_scat.png)   
#   
# ## Correlations  
#   
# Now we will look at correlated features using the `correlations` widget.  
#   
# ![correlations](./correlations.png)   
#   
# We see from the results of the widget that body mass and flipper length are most 
# closely correlated.  
#   
# # Pipeline B  
#
# ## Model comparison  
#      
# In the second part of the lab we are building an actual ML pipeline using linear 
# regression to predict body mass based on bill length, bill depth, flipper length, 
# a new engineered feature: bill ratio ($\text{bill ratio} = \frac{\text{bill length}}{\text{bill depth}}$)
#   
# After selecting appropriate numerical columns for regression, the data was ran through 
# a linear regression model with no regularization, and a linear regression with ridge 
# regularization. The screenshot below shows the results:  
#   
# ![results](./model_compare.png)  
#   
# We see from the results that ridge regularization had minimal effect on the results 
# from each model. We see that based on $\text{RMSE}$, our body mass predictions 
# are off by an average of $384 \text{grams}$. We also see that both models had an 
# $R^2$ value of $0.770$, which means that our model explains approximately $77\%$ 
# of the variation in body mass, which is a good predictive fit.   
#   
# ## Effect of Column Removal on $R^2$ value  
#   
# When experimenting with column removal and its effect on $R^2$, I discovered that 
# `flipper_length` had the greatest impact on $R^2$, knocking the value to $55\%$, 
# which is a significant blow. This matches our earlier discovery that flipper length 
# and body mass are closely correlated.  
#   
# ![experiment screenshot](./experiment.png)
