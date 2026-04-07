#################################################################################
#   Program Name: Dice Checker
#
#   Author: Lex Albrandt
#
#   Date: 07/07/25
#
#   File Name: die_test.py
#
#   Version: 1.1
#
#   File purpose: Glass box functionality testing for the die class
#################################################################################

import pytest
import time
from die import die

class Testdie:
    @pytest.fixture
    def die(self):
        return die()
    
    @pytest.fixture(autouse=True)
    def no_sleep(self, monkeypatch):
        monkeypatch.setattr(time, "sleep", lambda _: None)

    def test_die_initialization(self, die):
        assert die._num_samples == 0
        assert die._num_sides == 0
        assert die._deg_free == 0
        assert die._valid_choice == False
        assert die._side_list == []
        assert die._expected_freq == 0
        assert die._chi_squared_value == 0
        assert die._observed_value == 0
        assert die._p_value == 0
        assert die._significance_level == 0.05


    def test_get_sides_valid(self, die, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: 6)
        die.get_sides()
        assert die._num_sides == 20
        assert die._deg_free == 19
        assert die._num_samples == 100
        assert die._expected_freq == 5


    def test_get_sides_invalid(self, die, monkeypatch, capsys):
        inputs = iter(['-4', '0', '21', '6'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        
        die.get_sides()
        captured = capsys.readouterr()

        error_message = "Invalid input. Please make a choice between 1 and 6"
        error_count = captured.out.count(error_message)

        assert error_count == 3

        assert die._num_sides == 20


    def test_get_roll_entries_valid(self, die, monkeypatch):
        die._num_sides = 4
        die._num_samples = 20
        die._expected_freq = 5
        
        inputs = iter(['1'] * 2 + ['2'] * 8 + ['3'] * 4 + ['4'] * 6)
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        # Patch os.system to do nothing
        monkeypatch.setattr('os.system', lambda _: None)

        die.get_roll_entries()
        
        assert die._side_list[1] == 2
        assert die._side_list[2] == 8
        assert die._side_list[3] == 4
        assert die._side_list[4] == 6

        total_rolls = sum(die._side_list)
        assert total_rolls == 20

    
    def test_get_roll_entries_invalid(self, die, monkeypatch, capsys):
        die._num_sides = 4
        die._num_samples = 20
        die._expected_freq = 5
        
        inputs = iter(['1', '-1', '0', '5', '1'] + ['2'] * 8 + ['3'] * 4 + ['4'] * 6)
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        
        # Patch os.system to do nothing
        monkeypatch.setattr('os.system', lambda _: None)

        die.get_roll_entries()
        captured = capsys.readouterr()

        error_message = "Invalid input. You must enter a number between 1 and 4"
        error_count = captured.out.count(error_message)

        assert error_count == 3
        
        assert die._side_list[1] == 2
        assert die._side_list[2] == 8
        assert die._side_list[3] == 4
        assert die._side_list[4] == 6

        total_rolls = sum(die._side_list)
        assert total_rolls == 20


    # def test_get_roll_entries_valid(self, die, monkeypatch, capsys):
    #     die._num_sides = 4
    #     die._num_samples = 20
    #     die._expected_freq = 5
        
    #     inputs = iter(['2', '8', '4', '6'])
    #     monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        
    #     # Patch os.system to do nothing
    #     monkeypatch.setattr('os.system', lambda _: None)

    #     die.get_roll_entries()
        
    #     assert die._side_list[1] == 2
    #     assert die._side_list[2] == 8
    #     assert die._side_list[3] == 4
    #     assert die._side_list[4] == 6

    # def test_get_roll_entries_invalid(self, die, monkeypatch, capsys):
    #     die._num_sides = 4
    #     die._num_samples = 20
    #     die._expected_freq = 3
    #     die._valid_choice = True
        
    #     inputs = iter(['-2', '2', '8', '4', '6'])
    #     monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        
    #     # Patch os.system to do nothing
    #     monkeypatch.setattr('os.system', lambda _: None)

    #     die.get_roll_entries()
        
    #     captured = capsys.readouterr()
    #     assert "Number of rolls cannot be less than 0" in captured.out
        
    #     assert die._side_list[1] == 2
    #     assert die._side_list[2] == 8
    #     assert die._side_list[3] == 4
    #     assert die._side_list[4] == 6