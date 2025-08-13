#################################################################################
#   Program Name: Dice Checker
#
#   Author: Lex Albrandt
#
#   Date: 06/14/25
#
#   File Name: die.py
#
#   Version: 1.0
#
#   File purpose: Initialize all functions for the die class
#################################################################################

import textwrap
import os
import time
import scipy.stats as stats

class die:
    
    def __init__(self) -> None:
        """ Default constructor
        
            Returns: None
        """
        self._num_sides = 0
        self._num_samples = 0
        self._deg_free = 0
        self._valid_choice = False
        self._side_list = []
        self._chi_squared_value = 0
        self._expected_freq = 0
        self._observed_value = 0
        self._p_value = 0
        self._significance_level = 0.05


    def get_sides(self) -> None:
        """ Function to get the number of sides for the die the user wants to test
        
            Raises:
                ValueError: for invalid number of sides

            Returns: None
        """ 

        self._valid_choice = False
        
        number_print = textwrap.dedent(f"""
            How many sides does your die have:
            ----------------------------------
            1. 4
            2. 6
            3. 8
            4. 10
            5. 12
            6. 20\n""")

        while not self._valid_choice:
            try:
                print(number_print)
                num_choice = int(input("Please choose (1-6): "))
                if num_choice not in range(1, 7):
                    raise ValueError("Please make a choice between 1 and 6")

                match num_choice:
                    case 1:
                        self._num_sides = 4
                    case 2:
                        self._num_sides = 6
                    case 3:
                        self._num_sides = 8
                    case 4:
                        self._num_sides = 10
                    case 5:
                        self._num_sides = 12
                    case 6:
                        self._num_sides = 20

                self._valid_choice = True
                self._deg_free = self._num_sides - 1
                self._num_samples = self._num_sides * 5
                self._expected_freq = self._num_samples // self._num_sides

            except ValueError as e:
                print(f"Invalid input. {e}")

        print(f"\nThe number of rolls you need to perform for your die with {self._num_sides} sides is {self._num_samples}.")
        time.sleep(3)


    def print_initial_info(self) -> None:
        """ Function to print out the info based on user input

            Returns: None
        """

        info = textwrap.dedent(f"""
        Here is the info for your test:
        ---------------------------------
        Number of sides:        {self._num_sides}
        Degrees of Freedom:     {self._deg_free}
        Number of samples:      {self._num_samples}
        Expected Frequency:     {self._expected_freq}""")
        print(info)
        time.sleep(3)
    

    def get_roll_entries(self) -> None: 
        """ Function for the user to enter roll values
            for each side of the die
            
            Returns: None

            ValueError: invalid roll input, cannot be negative
        """

        total = 0
        self._side_list = [0] * (self._num_sides + 1)

        info = textwrap.dedent(f"""
        The next section of the test will ask you to enter the number of the 
        side for each roll. You will be given a tally at the end.""")
        print(info) 
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')

        while total < self._num_samples:
            try:
                num_entered = int(input(f"Enter the number you rolled: "))
                if num_entered not in range (1, self._num_sides + 1):
                    raise ValueError(f"You must enter a number between 1 and {self._num_sides}")
                self._side_list[num_entered] += 1
                total += 1
                print(f"You have {self._num_samples - total} rolls remaining\n")
                time.sleep(1)
                os.system('cls' if os.name == 'nt' else 'clear')     

            except ValueError as e:
                print(f"Invalid input. {e}")


    
    def compute_chi_squared(self) -> None:
        """ Function to compute the chi squared value for a given die
        
            Returns: None
        """
        self._chi_squared_value = 0

        for i in range(1, self._num_sides + 1):
            observed_value = self._side_list[i]
            self._chi_squared_value += ((observed_value - self._expected_freq) ** 2) / self._expected_freq

    
    def is_fair(self) -> None:
        """ Function to determine if the die is fair based on user provided values
            and calculated p-value

            Returns: None
        """

        self._p_value = 1 - stats.chi2.cdf(self._chi_squared_value, self._deg_free)
        p_val_info = textwrap.dedent("""
        In order for your die to be considered fair, we expect the p-value to be greater than
        or equal to 0.05. If the p-value from your test is less than 0.05 your die are not
        considered fair.\n""")
        print(p_val_info)
        time.sleep(3)
        print(f"The p-value for your die: {self._p_value:.2f}")
        if self._p_value < self._significance_level:
            print("Your die failed the chi-squared test!")
        else:
            print("Your die passed the chi-squared test!")

        self.print_results()

            
    def print_results(self) -> None:
        """ Function to print the results table for roll tallies
        
            Returns: None
        """
        print()
        print(f"{'Side number':<12} | {'Tally':<6}")
        print(f"{'-' * 12}-+-{'-' * 6}")
        for i in range (1, self._num_sides + 1):
            print(f"{i:<12} | {self._side_list[i]:<6}")
        print()
        print(f"{'Total Rolls':<12} | {sum(self._side_list):<6}")