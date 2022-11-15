import sys
import pickle

with open(sys.argv[1], 'rb') as model_file:
    model = pickle.load(model_file)
model.save_model(sys.argv[2])
