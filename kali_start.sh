#!/bin/bash

cd swertres/
python3 sw3_results_v1.py
python3 sw3_results_v2.py
python3 script_filter_excel.py
python3 script_filter_gap_excel.py
python3 script_diff_one_v2.3.1.py
python3 script_count_missing_v1.1.py

cd ../stl
python3 stl_results_v1.py
python3 stl_results_v2.py
python3 script_filter_excel.py
python3 script_filter_gap_excel.py
python3 script_diff_one_v2.3.1.py
python3 script_count_missing_v1.1.py

cd ../swertres
python script_current_results.py

cd ../stl
python script_current_results.py
