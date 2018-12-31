clear
echo "Fetching SW3 and STL results."
cd ~/gidapp/swertres
python sw3_results_v1.py
python sw3_results_v2.py
am start -a android.intent.action.VIEW -d file://~/sdcard/gidapp/swertres/results_v2.txt -t text/plain --activity-clear-task
cd ~/gidapp/stl
python stl_results_v1.py
python stl_results_v2.py
cd ~
echo "Exiting program in 30 seconds."
sleep 30s
killall com.termux
