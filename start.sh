#!/data/data/com.termux/files/usr/bin/env bash

clear
echo "PROCESSING SW3:"
cd /sdcard/Download/gidapp/swertres
echo
echo "Fetching results:"
python sw3_results_v1.py
python sw3_results_v2.py
echo
#echo "SUM Digits Pattern V2:"
#python sum_digits_v2.1.py
#echo
echo "SYNC Digits Pattern V2:"
python pair_digits_v2.1.py
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
python sw3_results_v1.py
python sw3_results_v2.py
echo
#echo "SUM Digits Pattern V2:"
#python sum_digits_v2.1.py
#echo
echo "SYNC Digits Pattern V2:"
python pair_digits_v2.1.py
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
	echo "Exiting program in 30 seconds."
	sleep 30s
	killall com.termux
fi
