#!/bin/bash

cd swertres/
python sw3_results_v1.py
python sw3_results_v2.py

cd ../stl
python stl_results_v1.py
python stl_results_v2.py

cd ../swertres
python script_current_results.py

cd ../stl
python script_current_results.py

cd ../swertres
python script_spot_patterns_v1.py
python script_spot_patterns_v2.py
python script_common_combi_pair.py

cd ../stl
python script_spot_patterns_v1.py
python script_spot_patterns_v2.py
python script_common_combi_pair.py