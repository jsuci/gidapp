#!/data/data/com.termux/files/usr/bin/env bash

clear
echo "PROCESSING SW3:"
cd /sdcard/Download/gidapp/swertres
echo
echo "Fetching Results:"
python sw3_results_v1.py
python sw3_results_v2.py
python script_filter_excel.py
echo
echo
echo "SEQ_TYPES Pattern"
python script_diff_one_v2.3.py
python script_diff_one_v2.4.py
python script_count_missing_v1.1.py
echo
echo
echo
echo
echo "PROCESSING STL:"
cd /sdcard/Download/gidapp/stl
echo
echo "Fetching Results:"
python stl_results_v1.py
python stl_results_v2.py
python script_filter_excel.py
echo
echo
echo "SEQ_TYPES Pattern"
python script_diff_one_v2.3.py
python script_diff_one_v2.4.py
python script_count_missing_v1.1.py
echo
echo
echo "Current SW3 Results:"
cd /sdcard/Download/gidapp/swertres
python script_current_results.py
echo
echo
echo "Current STL Results:"
cd /sdcard/Download/gidapp/stl
python script_current_results.py
echo
echo
#am start -a android.intent.action.VIEW -d file://~/sdcard/Download/gidapp/swertres/results_v2.txt -t text/plain --activity-clear-task
read -p "Press enter to exit: " -n 1 -r
if [[ $REPLY =~ ^$ ]]
then
 killall com.termux
fi
echo
# echo -ne "\n" | killall com.termux