#################################################################################
#   Program Name: Dice Checker
#
#   Author: Lex Albrandt
#
#   Date: 06/13/25
#
#   File Name: compute_test.py
#
#   Version: 1.0
#
#   File purpose: Glass box functionality testing for the Compute class
#################################################################################

import pytest
from Compute import Compute

class TestCompute:
    @pytest.fixture
    def compute(self):
        return Compute()

    def test_compute_initialize(self, compute):
        assert compute._num_sides == 0
        assert compute._num_samples == 0
        assert compute._deg_free == 0
        assert compute._expect_freq == 0
        assert compute._text_input == ''
        assert compute._int_input == 0
        assert compute._valid_choice == False
        assert isinstance(compute._chi_square_dict, dict)
        

        expected_dict = {
            4 : (7.815,  3),
            6 : (11.070, 5),
            8 : (14.067, 7), 
            10 : (16.919, 9),
            12 : (19.675, 11),
            20 : (30.144, 19)}

        assert compute._chi_square_dict == expected_dict