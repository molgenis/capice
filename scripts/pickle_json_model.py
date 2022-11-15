import sys
import pickle
import xgboost as xgb

model = xgb.XGBClassifier()
model.load_model(sys.argv[1])
with open(sys.argv[2], 'wb') as model_dump:
    pickle.dump(model, model_dump)
