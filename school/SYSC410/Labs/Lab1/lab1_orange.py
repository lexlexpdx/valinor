# %% [markdown]
# Lex Albrandt  
# SYSC 410  
# Lab 1  
#   
#   
# # Using Orange Framework  
#   
# ## Data Import and Data Table  
#   
# Data was loaded with CSV load and a data table was generated with the following results:  
#   
# There are 344 rows with approximately $0.8\%$ missing data.  
#   
# ![Penguins Data Table](./screenshots/data_table.png)
#
#
# ## Scatter Plot  
#   
# A scatter plot was added showing clear cluster separation (with a small amount of overlap) between 
# the Adelie, Chinstrap, and Gentoo species.  
#   
# ![Penguins Scatter Plot](./screenshots/scatter_plot.png)
#   
#   
# ## Select Columns  
#   
# Columns were selected as shown in the screenshot below:  
#   
# ![Penguins Column Select](./screenshots/select_col.png)  
#   
#   
# ## Train/Test split  
#   
# A train/test split of $80{\%}$ training, $20\%$ testing data was performed as below:  
#   
# ![Penguins train/test split](./screenshots/data_split.png)  
#   
#    
# ## KNN settings 
#   
# KNN settings were added with $k=5$ and a Euclidean metric as below:  
#   
# ![Penguins KNN](./screenshots/knn.png)   
#   
#   
# ## Test and Score  
#   
# Test and score was wired according to the specifications in class and had the 
# following output:   
#   
# ![Penguins test and score](./screenshots/eval.png)  
#   
# We can see that the classification accuracy is around $82\%$, which is decent 
# for a simple KNN, but we also want to understand where the model is misclassifying 
# the data, so we will also craft a confusion matrix.  
#   
#   
# Confusion Matrix  
#   
# ![Penguins confusion and scatter](./screenshots/conf_scat.png)  
#   
# From the screenshot above we can see that the model does a decent job at classifying 
# the species correctly, but misclassifies $25\%$ of Adelie penguins as Chinstrap penguins. 
# Similarly, Chinstrap penguins are misclassified as Adelie penguins about $14\%$ of the time. 
#   
#   
# ## Iteration over K values
#   
# To see if we can find the best accuracy for our KNN model, we need to iterate 
# over our values of $k$ to determine which value corresponds to the highest accuracy, 
# which also takes the confusion matrix into account, because accuracy is not only 
# determined by which classifications the model gets right, but where it misclassifies 
# as well.  
#   
# In the table below we can see that the "sweet spot" for the $k$ value that gives 
# the best accuracy as well as minimizes misclassification is $k=6$.   
#   
# ![Penguins table](./screenshots/k_iterations.png)  
#   
# It is difficult to differentiate between $k=5$ and $k=6$ based solely on the classification 
# accuracy, but when consulting the confusion matrix for $k=6$ we see that the misclassifcation 
# of Adelie penguins as Chinstrap penguins is still around $25\%$, but the misclassification 
# of Chinstrap as Adelie penguins drops to $0\%$, however, the misclassification 
# of Gentoo penguins as either Adelie or Chinstrap increases. This points to needing to 
# consult other metrics (Like the F1 score) to more accuractly determine the "sweet spot".
#   
# ![Penguins Confusion Matrix](./screenshots/k_6_conf.png)
#   
# # Using Python with Google Colab  
#   
# Below are the screenshots from the jupyter notebook using Google Colab  
#   
# ## EDA Observations  
#   
# ![EDA observations](./screenshots/eda_obs_jup.png)  
#   
# ## Evaluate  
#   
# ![Evaluate](./screenshots/eval_jup.png)  
#   
# ## Reflect  
#   
# ![Reflect](./screenshots/reflect.png)   
#   
# # Lab Reflections
#   
# ## Which felt faster for exploring the data?  
#   
# It was much faster to visualize the data in Orange.  
#   
# ## Which gave you a better sens of what the model was doing?  
#   
# I think Orange was better for visualizing what is happening with data flow in 
# the model.  
#   
# ## Which would you rather hand to a colleague to reproudce your analysis?  
#   
# Jupyter notebooks are far and away superior for reproducibility and explainantion 
# of steps and results. I also prefer using Python generally because I am a 
# Computer Science major. 
