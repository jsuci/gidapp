#!/data/data/com.termux/files/usr/bin/env bash

clear
echo "FETCHING SW3 RESULTS:"
cd /sdcard/Download/gidapp/swertres
python sw3_results_v1.py
python sw3_results_v2.py
echo
echo "FETCHING STL RESULTS:"
cd /sdcard/Download/gidapp/stl
python stl_results_v1.py
python stl_results_v2.py
echo
echo
echo
echo
echo "SUM RESULTS SW3:"
cd /sdcard/Download/gidapp/swertres
python sum_digits_v2.1.py
echo
echo "SUM RESULTS STL:"
cd /sdcard/Download/gidapp/stl
python sum_digits_v2.1.py
echo
echo
echo
echo
echo "PAIR RESULTS SW3:"
cd /sdcard/Download/gidapp/swertres
python pair_digits_v2.1.py
echo
echo "PAIR RESULTS STL:"
cd /sdcard/Download/gidapp/stl
python pair_digits_v2.1.py
echo
echo
echo
echo
echo "CURRENT RESULTS SW3:"
cd /sdcard/Download/gidapp/swertres
python current_results.py
echo
echo "CURRENT RESULTS STL:"
cd /sdcard/Download/gidapp/stl
python current_results.py
cd ~
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
