#!/bin/bash

cd swertres/
python3 sw3_results_v1.py
python3 sw3_results_v2.py
python3 script_count_missing.py

cd ../stl
python3 stl_results_v1.py
python3 stl_results_v2.py
python3 script_count_missing.py

cd ../swertres
python script_current_results.py

cd ../stl
python script_current_results.py
