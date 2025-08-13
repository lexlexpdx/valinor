#################################################################################
#   Program Name: Dice Checker
#
#   Author: Lex Albrandt
#
#   Date: 06/13/25
#
#   File Name: dice_checker.py
#
#   Version: 1.0
#
#   File purpose: Serves as the main file for the dice checker program
#################################################################################

from Menu import Menu
from die import die
import os
    
        
def main():
    my_die = die()
    menu = Menu(my_die)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    menu.execute_menu()
    
if __name__ == "__main__":
    main()