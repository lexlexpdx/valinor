# %% [markdown]
# Lex Albrandt  
# SYSC410  
# Lab 7  
#  
# ## Architecture comparison screenshot  
# ![comp table](./screenshots/all_comps.png)  
#   
# As seen in the table above the best architecture of all the neural networks was 
# the single layer perceptron with a hidden layer of 50 neurons.  
#   
# # Reflection Questions  
# 1. Did adding more hidden layers improve accuracy on Penguins? Why might a 
# small dataset with a handful of features not benefit from deeper architectures?
#
# Adding more hidden layers did not improve accuracy. This is because it is a small 
# dataset, because the model is much more likely to overfit, leading to poor generalization.  
#   
# 2.  Compare the neural network’s accuracy to Random Forest and SVM on this same 
# dataset. Is the difference large enough to justify the added complexity? When 
# might a neural network become the clear winner?  
#   
# We can see in the comparison table above that Random Forest and SVM performed 
# comparably well to all single layer perceptron architectures on this dataset. 
# Given the computational cost and code complexity (if we were actually coding this 
# in python with pytorch or keras), the small increase in accuracy metrics does 
# not justify the added complexity. A neural network would likely be a clear winner 
# with a much more complex and robust dataset (far more than 1500 entries).  
#   
# 3. Unlike a Decision Tree or feature importance ranking, a neural network doesn’t 
# directly tell you which features matter. In a natural science context — say, 
# classifying rock types or bird species — why might that lack of interpretability 
# be a real problem, not just an inconvenience?  
#   
# Goal in natural science is not just to predict accurately, but to also 
# understand the underlying phenomena that are causing certain traits to increase 
# classification or prediction accuracy. Because the inner workings of neural networks 
# and how they update weights and biases between each layer, especially in more complex 
# models like convolutional neural networks, it can be a detriment to not know which 
# biological traits are actually contributing to accuracy. 
