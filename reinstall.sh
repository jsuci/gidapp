echo "Installing files and dependencies..."
apt update
apt upgrade
pkg install python
pkg install git
pip install requests
pip install bs4
pip install openpyxl
pip install flake8
pip install autopep8