#!/bin/bash

cd swertres
python sw3_results_a_v1.py
python sw3_results_b_v3.py

python script_digit_position.py

python script_excel_results_2.py
python script_excel_results_3.py
python script_excel_results_4.py -s
python script_excel_results_5.py
python script_gap_common_pair.py

python script_duplicate_pairs.py