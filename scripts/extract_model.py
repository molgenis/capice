"""
Script that extracts the model in json format from a .pickle.dat model file.

Usage:
python3 extract_model.py <input.pickle.dat> <output.json>

IMPORTANT:
This script must be executed while the CAPICE version is installed that was used to generate the
.pickle.dat model file!!!
"""
import sys
import pickle

with open(sys.argv[1], 'rb') as model_file:
    model = pickle.load(model_file)
model.save_model(sys.argv[2])
