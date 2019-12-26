#!/bin/bash

clear
echo "PROCESSING SW3:"
cd /sdcard/Download/repo/gidapp/swertres
echo
echo "Fetching Results:"
python sw3_results_v1.py
python sw3_results_v2.py
echo
echo
echo "PROCESSING STL:"
cd /sdcard/Download/repo/gidapp/stl
echo
echo "Fetching Results:"
python stl_results_v1.py
python stl_results_v2.py
echo
echo
echo "CURRENT RESULTS:"
echo
echo "Current SW3 Results:"
cd /sdcard/Download/repo/gidapp/swertres
python script_current_results.py
echo
echo "Current STL Results:"
cd /sdcard/Download/repo/gidapp/stl
python script_current_results.py
echo
echo
echo "GENERATE PROBABLES"
echo
echo "SW3 Probables:"
cd /sdcard/Download/repo/gidapp/swertres
python script_spot_patterns.py
python script_common_combi_pair.py
echo
echo "STL Probables:"
cd /sdcard/Download/repo/gidapp/stl
python script_spot_patterns.py
python script_common_combi_pair.py
read -p "Press enter to exit: " ext
if [ -z $ext ]
then
 killall com.termux
fi
echo
# echo -ne "\n" | killall com.termux