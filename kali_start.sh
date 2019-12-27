#!/bin/bash

cd swertres/
python3 sw3_results_v1.py
python3 sw3_results_v2.py

cd ../stl
python3 stl_results_v1.py
python3 stl_results_v2.py

cd ../swertres
python3 script_current_results.py

cd ../stl
python3 script_current_results.py

cd ../swertres
python3 script_spot_patterns_v1.py
python3 script_spot_patterns_v2.py
python3 script_common_combi_pair.py

cd ../stl
python3 script_spot_patterns_v1.py
python3 script_spot_patterns_v2.py
python3 script_common_combi_pair.py
