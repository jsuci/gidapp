#!/data/data/com.termux/files/usr/bin/env bash

clear
echo "PROCESSING SW3:"
cd /sdcard/Download/gidapp/swertres
echo
echo "DIFF_ZERO Pattern V1.1"
python script_diff_zero_v1.1.py
# echo "SYNC Digits Pattern V2.4:"
# python script_sync_digits_v2.4.py
# echo
# echo "SOLID Pattern V1.2:"
# python script_solid_pattern_v1.2.py
echo
echo "Fetching Results:"
python sw3_results_v1.py
python sw3_results_v2.py
echo
echo "Current Results:"
python script_current_results.py
echo
# echo "SUM Digits Pattern V2.1:"
# python sum_digits_v2.1.py
# echo
# echo "SYNC Digits Pattern V1.1:"
# python sync_digits_v1.1.py
# echo
#echo "MISSING Digits Pattern V2.1:"
#python missing_digits_v2.1.py
echo
echo
echo
echo
echo "PROCESSING STL:"
cd /sdcard/Download/gidapp/stl
echo
echo "DIFF_ZERO Pattern V1.1"
python script_diff_zero_v1.1.py
# echo "SYNC Digits Pattern V2.4:"
# python script_sync_digits_v2.4.py
# echo
# echo "SOLID Pattern V1.2:"
# python script_solid_pattern_v1.2.py
echo
echo "Fetching Results:"
python stl_results_v1.py
python stl_results_v2.py
echo
echo "Current Results:"
python script_current_results.py
echo
# echo "SUM Digits Pattern V2.1:"
# python sum_digits_v2.1.py
# echo
# echo "SYNC Digits Pattern V1.1:"
# python sync_digits_v1.1.py
# echo
#echo "MISSING Digits Pattern V2.1:"
#python missing_digits_v2.1.py
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