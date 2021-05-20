#!/bin/bash

cd swertres
python sw3_results_a_v1.py
python sw3_results_b_v3.py

python script_digit_position.py
python script_digit_pair.py
python script_digit_gap_pair.py

python script_excel_results.py
python script_excel_results_2.py
python script_excel_results_3.py

python script_odd_even_big_small.py
python script_duplicate_pairs.py