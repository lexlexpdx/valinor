# %% [markdown]
# Lex Albrandt  
# SYSC410  
# Lab3  
#   
# ![Your Turn 1](./screenshots/yourturn1.png)
#   
# ![Your Turn 2](./screenshots/yourturn2.png)
#   
# ![Your Turn 3](./screenshots/yourturn3.png)  
#   
# ![comparison table](./screenshots/comparison_table.png)  
#   
# ![confusion matrix](./screenshots/nb_conf_mat.png)  
#   
# ## Classifier recommendation  
#   
# I would recommend either logistic regression or KNN based on their accuracy performance 
# in both the single sample training and k-fold cross-validation. Because the penguins 
# dataset is linearly separable, either of these models perform very well, especially 
# with engineered features that futher separate classes.  
#   
# ## Reflection Questions
#   
# 1. The logistic regression and KNN performed equally well. I would not necessarily 
# expect the same winner with a different dataset because the penguins dataset is 
# linearly separable from the start. If the dataset was not linearly separable I do not 
# think that KNN and logistic regression would perform as well.  
# 2. Addition or removal of `island` and `sex` categories didn't really move the accuracy 
# a noticable amount. It was the same across all three models.  
# 3. I chose to use the confusion matrix for Naive Bayes, even though it wasn't the 
# *best* model to illustrate that even though the model had a slightly lower accuracy, 
# the confusion matrix shows that it there the model had a trivial amount of error. 
# I think the biological measurement that would overlap would either be the bill length 
# or body mass (based on the scatter plot).
