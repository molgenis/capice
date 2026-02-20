import json
import xgboost as xgb

REQUIRED_BOOSTER_ATTRS = ["CAPICE_version", "vep_features", "processable_features"]

# Optional: decode JSON fields
def maybe_json(s):
    try:
        return json.loads(s)
    except Exception:
        return s

class ModelValidator:
    @staticmethod
    def validate_has_required_attributes(model: xgb.Booster):
        """
        Validate presence and (optionally) structure of required Booster attributes.
        Raises AttributeError / ValueError on problems.
        """
        attrs = model.attributes() or {}
        missing = [k for k in REQUIRED_BOOSTER_ATTRS if k not in attrs]
        if missing:
            raise AttributeError(f"Missing Booster attribute(s): {', '.join(missing)}")


        return {
            "CAPICE_version": attrs["CAPICE_version"],
            "vep_features": maybe_json(attrs["vep_features"]),
            "processable_features": maybe_json(attrs["processable_features"]),
        }
