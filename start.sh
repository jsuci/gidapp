#!/data/data/com.termux/files/usr/bin/env bash

clear
echo "PROCESSING SW3:"
cd /sdcard/Download/gidapp/swertres
echo
echo "SEQ_TYPES Pattern"
python script_seq_types_v1.1.py
python script_seq_types_v2.1.py
echo
echo "Fetching Results:"
python sw3_results_v1.py
python sw3_results_v2.py
python script_filter_excel.py
echo
echo "Current Results:"
python script_current_results.py
echo
echo
echo
echo
echo
echo "PROCESSING STL:"
cd /sdcard/Download/gidapp/stl
echo
echo "SEQ_TYPES Pattern"
python script_seq_types_v1.1.py
python script_seq_types_v2.1.py
echo
echo "Fetching Results:"
python stl_results_v1.py
python stl_results_v2.py
python script_filter_excel.py
echo
echo "Current Results:"
python script_current_results.py
echo
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