#!/bin/bash

cd swertres
python sw3_results_a_v1.py
python sw3_results_b_v3.py

python script_digit_position.py
python script_digit_pair.py
python script_digit_gap_pair.py

python script_excel_results.py