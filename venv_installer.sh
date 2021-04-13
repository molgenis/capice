#!/bin/bash
echo "Checking venv direction"
if [ ! -d './venv' ]
then
  echo "Creating virtual environment"
  python3 -m venv ./venv
else
  echo "Virtual environment present"
fi
echo "All done! Do not forget to activate the venv using:"
echo "source './venv/bin/activate'"
