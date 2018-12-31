clear
echo "Fetching SW3 and STL results."
cd ~/gidapp/swertres
python sw3_results_v1.py
python sw3_results_v2.py
cd ~/gidapp/stl
python stl_results_v1.py
python stl_results_v2.py
cd ~
echo "Exiting program in 30 seconds."
sleep 30s
killall com.termux
