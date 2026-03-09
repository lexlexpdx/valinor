# %% [markdown]
# Lex Albrandt  
# CS445  
# HW 4  
#   
# # Quesiton 1  
#   
# ### 1a)  
#   
# $\text{hidden units }N_h = 2 \text{, output units } N_o = 1$
#   
# ### 1b)  
#   
# $z^H = \begin{bmatrix}1 \\ 1 \end{bmatrix}x + \begin{bmatrix}-1 \\ -3\end{bmatrix}$  
#   
# $z^H = \begin{bmatrix} x \\ x \end{bmatrix}+ \begin{bmatrix} -1 \\ -3 \end{bmatrix} = \begin{bmatrix} x-1 \\ x-3 \end{bmatrix}$
#   
# ### 1c)  
# $u_{H_1} = \begin{cases}
# 1 & x \ge 1 \\
# 0 & x < 1 \end{cases}$,    
# $u_{H_2} = \begin{cases}
# 1 & x \ge 3 \\
# 0 & x < 3 \end{cases}$
#   
# ### 1d)  
# $z^o = -u_{H_1}(x) + 2u_{H_2}(x) + 0.5$
#  
# ### 1e)  
# for $x < 1: u_{H_1} = 0 \text{, }u_{H_2}=0$  
# Thus $z^o = -1(0) + 2(0) + 0.5 = 0.5 \ge 0 \Rightarrow \hat{y} = 1$  
# for $ 1 \ge x \ge 3: u_{H_1} = 1, u_{H_2} = 0$  
# Thus $z^o = -1(1) + 2(0) + 0.5 = -0.5 < 0 \Rightarrow \hat{y} = 0$
# for $x \ge 3: u_{H_1} = 1 \text{, }u_{H_2}=1$  
# Thus $z^o = -1(1) + 2(1) + 0.5 = 1.5 \ge 0 \Rightarrow \hat{y} = 1$  
#   
# $\hat{y} = \begin{cases}
# 1 \text{   } x < 1 \\
# 0 \text{   }1 \le x < 3 \\
# 1 \text{   }x \ge 3 \end{cases}$
#   
# # Question 2  
#   
# 2a and 2b)
#  
# for $x < 2: u_{H_1} = 0 \text{, }u_{H_2}=0$  
# Thus $z^o = W_1(0) + W_2(0) + b_0 = b_0$  
# for $ 2 \ge x \ge 4: u_{H_1} = 1, u_{H_2} = 0$  
# Thus $z^o = W_1(1) + WS_2(0) + b_0 = W_1 + b_0$  
# for $x \ge 4: u_{H_1} = 1 \text{, }u_{H_2}=1$  
# Thus $z^o = W_1(1) + W_2(1) + b_0 = W_1 + W_2 + b_0$  
#  
# $\hat{y}(x) = 
# \begin{cases}
# 0 & x < 2 \quad z_o = b_0 < 0 \\
# 1 & 2 \le x < 4, \quad z_0 = W_1 + b_0 \ge 0 \\
# 0 & x \ge 4, \quad z_0 = W_1 + W_2 + b_0 \ge 0
# \end{cases}$   
#   
# For our dataset:  
# $x = 0,1 \Rightarrow b_0 < 0$
# $x = 3 \Rightarrow W_1 + b_0 \ge 0$  
# $x = 5 \Rightarrow W_1 + W_2 + b_0 < 0$  
#   
# We will determine the bounds for each of the parameters:  
# $b_0 < 0$  
# $W_1 \ge b_0$  
# $W_2 < -(W_1 + b_0)$  
#   
# We can choose parameters that fit within the bounds:  
# let $b_0 = -1, W_1 = 1, W_2 = -1$  
#   
# Then verify:  
# $x = 0 \Rightarrow \hat{y} = 0 = 1(0) - 1(0) -1 = -1 \Rightarrow 0 \checkmark$  
# $x = 1 \Rightarrow \hat{y} = 0 = 1(0) - 1(0) -1 = -1 \Rightarrow 0 \checkmark$
# $x = 3 \Rightarrow \hat{y} = 1 = 1(1) - 1(0) -1 = 0 \Rightarrow 1 \checkmark$  
# $x = 5 \Rightarrow \hat{y} = 0 = 1(1) - 1(1) -1 = -1 \Rightarrow 0 \checkmark$
#   
# ### 2c)  
# $x = 3.5 \Rightarrow u_{H_1} = 1, u_{H_2} = 0 \quad \Rightarrow \hat{y} = 1(1) - 1(0) -1 = 0 \Rightarrow 0$  
#   
# # Question 3  
#   
# ### 3a)  
# Start with the hidden layer formula:  
# $z_H = W_{H}x + b_H  
#   
# $z_{H_1} = (1)x_1 + (0)x_2 + 0 = x_1$
# $z_{H_2} = (0)x_1 + (1)x_2 + 0 = x_2$  
# $z_{H_3} = (1)x_1 + (1)x_2 - 1 = x_1 + x_2 - 1$  
#   
# Then find $u_{H_j}$ values:  
# $u_{H_1} = \begin{cases} 1 & x_1 \ge 0 \\ 0 & x_1 < 0 \end{cases}$
#   
# $u_{H_2} = \begin{cases} 1 & x_2 \ge 0 \\ 0 & x_2 < 0 \end{cases}$  
#   
# $u_{H_3} = \begin{cases} 1 & x_1 + x_2 \ge 1 \\ 0 & x_1 + x_2 < 1 \end{cases}$  
#   
# for $u_{H_1}$ the boundary is $x_1=0$, which is a vertical line, so $u_{H_1} = 1$ to the right of  
# the vertical line at $x_1 = 0$  
# for $u_{H_2}$ the boundary is $x_2=0$, which is a horizontal line, so $u_{H_2} = 1$ above the horizontal  
# line at $x_2 = 0$  
# for $u_{H_3}$ the boundary is $x_2 = -x_1 + 1$, which is a diagonal line with a slope of -1 and intercept of 1,  
# so $u_{H_3} = 1$ above that diagonal line  
#   
# ### 3b)  
# $z^o = (1)u_{H_1} + (1)u_{H_2} - (1)u_{H_3} - 1.5$  
# $z^o = u_{H_1} + u_{H_2} - u_{H_3} - 1.5$  
# when $\hat{y} = 1 \quad z^o \ge 0$  
# thus $u_{H_1} + u_{H_2} - u_{H_3} - 1.5 \ge 0$  
# $u_{H_1} + u_{H_2} - u_{H_3} \ge 1.5$  
#   
# So we need values that satisfy the above inequality:  
# let $u_{H_1} = 1, u_{H_2} = 1, u_{H_3} = 0$ then:
# $1 + 1 - 0 = 2 \ge 1.5 \checkmark$  
#   
# # Question 4
#   
# ### 4a)  
# For $N_i$, we have a 20 x 20 image, so we would first flatten it to a 1D vector, thus:  
# $N_i = 20 \cdot 20 = 400$  
# For $N_o$, we are looking for discrete letters of the alphabet, so:  
# $N_o = 26$  
# $N_h$ should be somewhere near $\frac{2}{3}$ of the input layer, so a reasonable choice  
# would be:  
# $N_h = 250$  
# A good choice for $g_{act}$ in this case would be ReLU: $g(z) = max{0,z}$  
# Because this is a multi-class classification problem $g_{out}$ would be softmax.  
#   
# ### 4b)  
# $N_i = 120$  
# $N_h = 80$  
# $N_o = 1$ for binary classification  
# $g_{act} = \text{ReLU}$  
# $g_{out} = \text{sigmoid}$ because it is a binary classification problem  
#   
# ### 4c)  
# $N_i = 5$  
# $N_h = 10$  
# $N_o = 1$  
# $g_{act} = \text{ReLU}$  
# $g_{out} = \text{linear}$ for regression
