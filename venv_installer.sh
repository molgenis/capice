#!/bin/bash
echo "Checking venv direction"
if [ ! -d './venv' ]
then
  mkdir venv
  cd venv
  echo "Creating virtual environment"
  python3 -m venv ./
  cd ..
else
  echo "Virtual environment present"
fi
echo "Checking and installing required packages"
source "./venv/bin/activate"
pip install scipy
pip install -r requirements.txt
echo "All done! Do not forget to activate the venv using:"
echo "source './venv/bin/activate' (you can use ctrl+shift+c to copy the command)"
