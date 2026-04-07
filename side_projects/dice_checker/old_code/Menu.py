#################################################################################
#   Program Name: Dice Checker
#
#   Author: Lex Albrandt
#
#   Date: 06/13/25
#
#   File Name: Menu.py
#
#   Version: 1.0
#
#   File purpose: Initializes all functions associated with the Menu Class
#################################################################################

import textwrap
from die import die

class Menu:

    def __init__(self, die: die):
        """ Default constructor. Uses dependency injection for the 
            Compute class and die class

            Args:
                compute (Compute): Compute class object
                die (die): die class object

            Returns:
                None 
        """
        self._user_choice = 0
        self._quit_choice = ''
        self._die = die
        self._valid_number = False

    
    def print_welcome(self) -> None:
        """ Function to print the welcome message

            Returns: None
        """

        welcome = textwrap.dedent("""
            Welcome to the Dice Checker! This program will help you determine if your new
            set of dice is fairly weighted.""")
        print(welcome)
    

    def print_description(self) -> None:
        """ Function to print the program description
        
            Returns: None
        """

        description = textwrap.dedent("""
            The program uses the Pearson's chi-square test from statistics that computes
            a number that indicates the probability that the sides of the die are rolled
            randomly. If you would like more info on the test here is the Wikipedia page:

            https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test

            There is also a blog post detailing the process at:

            https://deltasdnd.blogspot.com/2009/02/testing-balanced-die.html?m=1

            Let's start testing your new dice!""")
        print(description)


    def print_menu(self) -> None:
        """ Function to print the main menu
        
            Returns: None
        """

        menu = textwrap.dedent("""
              Menu
              ----------------------
              1. Start test
              2. Print tally table
              3. Quit
              """)
        print(menu)
    

    def print_exit(self) -> None:
        """ Function to print the exit message

            Returns: None
        """

        print(f"Thanks for using the Dice Checker! Happy rolling!")


    def get_user_choice(self) -> int:
        """ Function to get the user choice. Also ensures the user does
           not quit when they are not intending to

            Raises:
                ValueError: for invalid text option input

            Returns:
                int: user choice
        """

        self._user_choice = int(input(f"Please make a menu choice: "))
        if self._user_choice == 3:
            while self._quit_choice != 'y' or self._quit_choice != 'n':
                try:
                    self._quit_choice = input("Are you sure you want to quit (y/n): ")
                    if self._quit_choice != 'y' and self._quit_choice != 'n':
                        raise ValueError
                    if self._quit_choice == 'y':
                        return 3
                    else:
                        return 0
                except ValueError:
                    print("Invalid input. Please enter 'y' or 'n'.")
            
        if self._user_choice < 1 or self._user_choice > 3:
            return -1

        return self._user_choice 


    def execute_menu(self) -> None:
        """ Function to execute the main menu

            Raises:
                ValueError: For an invalid menu choice 
            
            Returns: None 
        """

        self.print_welcome()
        self.print_description()

        # While the user is not choosing to exit
        while self._user_choice != 3:

            self.print_menu()

            try:
                self._user_choice = self.get_user_choice()

                # Invalid input
                if self._user_choice == -1:
                    raise ValueError
                
                # Option 1
                # Start test
                if self._user_choice == 1:
                    self._die.get_sides()
                    self._die.print_initial_info()
                    self._die.get_roll_entries()
                    self._die.compute_chi_squared()
                    self._die.is_fair()

                # Option 2
                # print chi-squared table
                if self._user_choice == 2:
                    self._die.print_results()

            except ValueError as error:
                print(f"Invalid input. Menu choice must be between 1 and 3. Try again.\n")
            
        self.print_exit()
