# %% [markdown]
# Lex Albrandt  
# SYSC410  
# Lab4  
#  
# ![Your turn 1](./screenshots/your_turn1.png)  
#   
# ![Your turn 2](./screenshots/your_turn2.png) 
#
# ![Your turn 3](./screenshots/your_turn3.png)  
#   
# ![model_comparison](./screenshots/model_comp.png)  
#   
# ![confusion matrix](./screenshots/conf_mat.png)  
#   
# ![feature importance](./screenshots/feat_imp.png)  
#   
#
# ## Reflection Questions  
#   
# 1. In `rf.feature_importances` the bill length is the most important feature. This is 
#   because this feature is what ultimately answers the harder questions for splitting 
#   the classes.  
# 2. In the depth experiment the tree test accuracy stops improving at a depth of 
#   5. This indicates that the dataset does not have as many high-level relationships 
#   that separate the data, meaning the dataset is fairly simple.  
# 3. The ensemble is likely to not be of help here because as we discussed in question 
#   2, the dataset lacks a large number of high-level relationships, so further splitting 
#   classes with more nodes in the tree would not be a benefit.
