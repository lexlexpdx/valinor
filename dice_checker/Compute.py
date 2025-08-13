#################################################################################
#   Program Name: Dice Checker
#
#   Author: Lex Albrandt
#
#   Date: 06/13/25
#
#   File Name: Compute.py
#
#   Version: 1.0
#
#   File purpose: Initializes all function associated with the Compute class
#################################################################################

import textwrap

class Compute:
    
    def __init__(self) -> None:
        """ Default constructor
        
            Returns: None
        """
        self._num_sides = 0
        self._num_samples = 0
        self._deg_free = 0
        self._expect_freq = 0   
        self._text_input = ''
        self._int_input = 0
        self._valid_choice = False
        

            
    def print_chi_square_table(self) -> None:
        """ Function to print the chi-squared table values
        
            Returns: None
        """

        print(f"{'Sides':<10}{'Chi-Squared Value':<23}{'Degrees of Freedom':<20}")
        print(f"-"*56)
        for sides, (chi_squared, degrees_of_freedom) in self._chi_square_dict.items():
            print(f"{sides:<10}{chi_squared:<23}{degrees_of_freedom:<20}") 

            

            
    
            
        
