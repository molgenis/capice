"""
Generate a .pickle.dat model file from a json model file.

Usage:
python3 pickle_json_model.py <input.json> <output.pickle.dat>

IMPORTANT:
This script must be executed while the CAPICE version is installed for which the .pickle.dat file
should be used with!
"""
import sys
import pickle
import xgboost as xgb

model = xgb.XGBClassifier()
model.load_model(sys.argv[1])
with open(sys.argv[2], 'wb') as model_dump:
    pickle.dump(model, model_dump)
