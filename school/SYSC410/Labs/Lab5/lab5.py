# %% [markdown]
# Lex Albrandt  
# SYSC410  
# Lab 5  
#  
# ![your turn1](./screenshots/your_turn1.png)  
#   
# ![your turn2](./screenshots/your_turn2.png)
#   
# ![your turn3](./screenshots/your_turn3.png)  
#   
# ![decision boundary](./screenshots/dec_bound.png)  
#   
# ![grid cv](./screenshots/grid_cv.png)  
#   
# ![comp_table](./screenshots/comp_table.png)  
#   
# ## Reflection Questions  
#   
# 1. The RBF kernel performed best out of all of the kernel options. The shape of 
#   the boundaries indicates that the RBF kernel takes more support vectors into account 
#   which would allow for better generalization.  
# 2. Changing $C$ did not have much effect on accuracy in this case. The tradeoff 
#   between a high $C$ value and a low $C$ value is potentially better accuracy in 
#   either case, but with the risk of overfitting (large $C$ value), and underfitting 
#   (small $C$ value).  
# 3. I would make a decision based on dimensionality of the data (RF for high dimensionality, 
#   SVM for lower dimensionality), as well consideration of need for feature importance 
#   ranking.
