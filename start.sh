#!/data/data/com.termux/files/usr/bin/env bash

clear
echo "PROCESSING SW3:"
cd /sdcard/Download/gidapp/swertres
echo
echo "Fetching Results:"
python sw3_results_v1.py
python sw3_results_v2.py
echo
echo "SUM Digits Pattern V2.1:"
python sum_digits_v2.1.py
echo
echo "SYNC Digits Pattern V2.1:"
python sync_digits_v2.1.py
echo
echo "SYNC Digits Pattern V1.1:"
python sync_digits_v1.1.py
echo
echo "MISSING Digits Pattern V2.1:"
python missing_digits_v2.1py
echo
echo "Current Results:"
python current_results.py
echo
echo
echo
echo
echo "PROCESSING STL:"
cd /sdcard/Download/gidapp/stl
echo
echo "Fetching results:"
python stl_results_v1.py
python stl_results_v2.py
echo
echo "SUM Digits Pattern V2.1:"
python sum_digits_v2.1.py
echo
echo "SYNC Digits Pattern V2.1:"
python sync_digits_v2.1.py
echo
echo "SYNC Digits Pattern V1.1:"
python sync_digits_v1.1.py
echo
echo "MISSING Digits Pattern V2.1:"
python missing_digits_v2.1py
echo
echo "Current Results:"
python current_results.py
echo
echo
echo
echo
#am start -a android.intent.action.VIEW -d file://~/sdcard/Download/gidapp/swertres/results_v2.txt -t text/plain --activity-clear-task
read -p "Do you want to exit? (Y/y): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
	echo
	echo "Exiting program in 5 seconds."
	sleep 5s
	killall com.termux
fi
