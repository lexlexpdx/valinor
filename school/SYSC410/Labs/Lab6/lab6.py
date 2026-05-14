# %% [markdown]
# Lex Albrandt  
# SYSC410  
# Lab 6  
#   
# ## Scatter plot with clusters  
#   
# ![k = 3 cluster](./screenshots/k3_clust_scat.png)
#   
# ## Scatter plot with species  
#   
# ![k = 3 species](./screenshots/k3_spec_scat.png)
#   
# ## Hierarchical Clustering  
#   
# ![hierarchical](./screenshots/hier_plot.png)
#  
# ## Silhouette Scores
#   
# ![silouhette](./screenshots/sil_scores.png)
#   
# ## Scree Plot  
#   
# ![scree](./screenshots/scree.png)
#   
# ## PCA Scatter Plot  
#   
# ![PCA](./screenshots/pca_scat.png)  
#   
# ![PCA loading](./screenshots/pca_load.png)
#   
#   
# # Reflection Questions  
#   
# 1. The K-means cluster agree with true labels in the areas where there is no 
#   overlap between the species. The features that could be driving disagreements are 
#   ones that do not easily distinguish classes of species.  
# 2. The value of k that gave the best silhouette score was $k=2$. This does not match 
#   the true number of species. This could be because there are two very distinct 
#   clusters between the Gentoo species and the combined cluster of Adelie and Chinstrap. 
#   In this particular instance it likely means that this particular algorithm might 
#   not be the best suited for the classification task.  
# 3. The two original features that contribute most to PC1 are the flipper length 
#   and body mass. This makes sense because Gentoo penguins are typically the heaviest 
#   species with the longest flippers. 

