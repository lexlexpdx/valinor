# %% [markdown]
# Lex Albrandt  
# SYSC10  
# Data Adventure 3  
#   
# # PCA Pipeline  
#  
# The first task of this data adventure is to explore PCA in orange. We move `class` 
# in the `select columns`, this prevents the PCA widget from clustering on the `class` 
# label, but allows us to keep them for comparison.  When 2 principal components are selected 
# they explain $61\%$ of the variance. Likewise, when 3 principal compoents are selected 
# they explain $71\%$ of the variance. When 4 principal components are selected they explain 
# $80\%$ of the variance. In the screenshot below, we can see that in order to achieve 
# $90\%$ explained variance we must have 6 principal components.  
#   
# ![90% variance](./screenshots/pca90pct_scree.png)  
#   
# **Key question:** Does reducing dimensionality help or hurt your model?  
# I would say that dimensionality reduction does not help the model in a meaningful 
# way. If it takes 6 of the 10 features to acheive $90\%$ variance explaination, PCA 
# is likely not the best choice for this dataset.  
#   
# Additionally, we can look at the `linear projection` widget to see which features 
# contribute most to each principal component:  
#   
# ![Linear Projecttion](./screenshots/lin_proj_pca.png)  
#   
# **Key question:** Which features load most heavily on each principal component?  
# From the plot we can see that `mag_g` contributes most to PC1, and `u_g` contributes 
# most to PC2.  
#   
# # Clustering Pipeline  
#   
# The next task of the data adventure is to build a k-means clustering pipeline. 
# We again keep `class` in the meta section of the `select columns` widget so k-means 
# is not silently clustering on classes.  In the k-means widget the optimal value is 
# $k=3$.  
#   
# ### K-means by class  
#   
# ![k-means](./screenshots/k3_class_scat.png)  
#   
# ### K-means by cluster  
#   
# ![k-means](./screenshots/k3_clust_scat.png)  
#   
# **Key question:** Do unsupervised clusters match your known labels? Where do they 
# disagree?  
# We can see from the plots above that k-means does an ok job, especially with the 
# `QSO` class, however, it mislabels `GALAXY` and `STAR`.   
#   
# # Comprehensive model comparison  
#   
# For the last task in this data adventure we are comparing metrics between 3 different 
# models: random forest, SVM, and logistic regression.  
#   
# ![model comparison](./screenshots/rf_lr_svm_comp.png)  
#   
# **Key question:** If your dataset is imbalanced, how much does the minority class 
# benefit from look at F1 instead of accuracy?  
# The dataset is not imbalanced, however we can see that random forest far outperformed 
# logistic regression and SVM across the board in all metrics, inluding F1 score. 
# This tells us that random forest is an accurate and useful model for understanding 
# this dataset.  
#   
# # PCA explanation 
#   
# PCA emphasizes variation in large dataset by using pattern analysis. It reduces 
# dimensionality of large datasets to make the data more easy to explore. It can 
# be useful for certain datasets if the dataset is linearly separable, but is particularly 
# useful in datasets that are not linearly separable it uses techniques like kernels 
# to find more meaningful separations in multi-dimensional space.   


