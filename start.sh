#!/data/data/com.termux/files/usr/bin/env bash

clear
echo "Fetching SW3 results."
cd /sdcard/Download/gidapp/swertres
python sw3_results_v1.py
python sw3_results_v2.py
echo
echo "Fetching STL results."
cd /sdcard/Download/gidapp/stl
python stl_results_v1.py
python stl_results_v2.py
echo
echo
echo "Process sum for SW3."
cd /sdcard/Download/gidapp/swertres
python sum_digits_v2.1.py
echo
echo "Process sum for STL."
cd /sdcard/Download/gidapp/stl
python sum_digits_v2.1.py
echo
echo
echo "Process pair for SW3"
cd /sdcard/Download/gidapp/swertres
python pair_digits_v2.1.py
echo
echo "Process pair for STL"
cd /sdcard/Download/gidapp/stl
python pair_digits_v2.1.py
echo
echo
echo "Current results for SW3"
cd /sdcard/Download/gidapp/swertres
python current_results.py
echo
echo "Current results for STL"
cd /sdcard/Download/gidapp/stl
python current_results.py
cd ~
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
